#pragma once

#include <pybind11/pybind11.h>
#include <iostream>
#include <memory>
#include <functional>

namespace py = pybind11;

#include "lemonator_interface.hpp"
#include "lemonator_proxy.hpp"

#include "ds1820.hpp"
#include "sr04.hpp"
#include "tcs3200.hpp"

std::unique_ptr<lemonator_interface> limo;

class debug_decorator : public hwlib::pin_out {
    hwlib::pin_out& pout;
    const char* en;
    const char* dis;

public:
    debug_decorator(hwlib::pin_out& pout, const char* en, const char* dis) : pout(pout), en(en), dis(dis) { }

    void write(bool v) override {
        if (v) {
            std::cout << en << std::endl;
        } else {
            std::cout << dis << std::endl;
        }

        pout.write(v);
    }

    void flush() override { }
};

class serial_decorator : public hwlib::pin_out {
    hwlib::pin_out& pout;

public:
    serial_decorator(hwlib::pin_out& pout) : pout(pout) { }

    void write(bool v) override {
        pout.write(v);
    }

    void flush() override { }
};

class cin_tap : public hwlib::istream {
    hwlib::istream& is;

public:
    cin_tap(hwlib::istream& is) : is(is) { }

    bool char_available() override {
        return is.char_available();
    }

    char getc() override {
        char c = is.getc();
        std::cout << "getc [" << c << "]" << std::endl;;
        return c;
    }
};

class cout_tap : public hwlib::ostream {
    hwlib::ostream& os;

public:
    cout_tap(hwlib::ostream& os) : os(os) { }

    void putc(char c) override {
        std::cout << "putc [" << c << "]" << std::endl;
        os.putc(c);
    }

    void flush() override { }
};

namespace py_interface {
    class lcd_wrapper {
        hwlib::ostream& os;

    public:
        lcd_wrapper(hwlib::ostream& os) : os(os) { }

        void pushString(const char* str) {
            os << str << hwlib::endl;
        }
    };

    class keypad_wrapper {
        hwlib::istream& is;

    public:
        keypad_wrapper(hwlib::istream& is) : is(is) { }

        char pop() {
            char c;
            is >> c;
            return c;
        }
    };

    template <class t_underlying_sensor, class t_read_function, t_read_function v_func>
    class sensor_wrapper {
        t_underlying_sensor& underlying_sensor;

    public:
        sensor_wrapper(t_underlying_sensor& sens) : underlying_sensor(sens) { }

        auto readValue() {
            return std::invoke(v_func, &underlying_sensor);
        }
    };

    template <class t_underlying_effector>
    class effector_wrapper {
        t_underlying_effector& underlying_effector;

    public:
        effector_wrapper(t_underlying_effector& eff) : underlying_effector(eff) { }

        void switchOn() {
            underlying_effector.write(1);
        }

        void switchOff() {
            underlying_effector.write(0);
        }
    };

    #define create_py_binding(cls, call_func) sensor_wrapper<cls, decltype(call_func), call_func>
    using distance_wrapper = create_py_binding(hwlib::sensor_distance, hwlib::sensor_distance::read_mm);
    using colour_wrapper = create_py_binding(hwlib::sensor_rgb, hwlib::sensor_rgb::read_rgb);
    using temperature_wrapper = create_py_binding(hwlib::sensor_temperature, hwlib::sensor_temperature::read_mc);
    using presence_wrapper = create_py_binding(hwlib::pin_in, hwlib::pin_in::read);
    #undef create_py_binding
}

PYBIND11_MODULE(lemonator, m) {

#define create_sensor(py_classname, cpp_wrapper, exposed_func) \
py::class_<py_interface::cpp_wrapper>(m, py_classname) \
    .def(#exposed_func, &py_interface::cpp_wrapper::exposed_func)
    create_sensor("LCD", lcd_wrapper, pushString);
    create_sensor("KeyPad", keypad_wrapper, pop);
    create_sensor("LevelSensor", distance_wrapper, readValue);
    create_sensor("ColourSensor", colour_wrapper, readValue);
    create_sensor("TemperatureSensor", temperature_wrapper, readValue);
    create_sensor("PresenceSensor", presence_wrapper, readValue);
#undef create_sensor

#define create_effector(py_classname, cpp_wrapper) \
py::class_<py_interface::cpp_wrapper>(m, py_classname) \
    .def("switchOn", &py_interface::cpp_wrapper::switchOn) \
    .def("switchOff", &py_interface::cpp_wrapper::switchOff)
    create_effector("SimpleEffector", effector_wrapper<hwlib::pin_out>);
#undef create_effector

    m.def("getLCD", [&](){
        static auto lcd = py_interface::lcd_wrapper(limo->lcd);
        return lcd;
    });

    m.def("getKeyPad", [&](){
        static auto keypad = py_interface::keypad_wrapper(limo->keypad);
        return keypad;
    });

    m.def("getDistance", [&](){
        static auto dist = py_interface::distance_wrapper(limo->distance);
        return dist;
    });

    m.def("getColour", [&](){
        static auto colour = py_interface::colour_wrapper(limo->color);
        return colour;
    });

    m.def("getTemperature", [&](){
        static auto temp = py_interface::temperature_wrapper(limo->temperature);
        return temp;
    });

    m.def("getPresence", [&](){
        static auto reflex = py_interface::presence_wrapper(limo->presence);
        return reflex;
    });

    m.def("getHeater", [&](){
        static auto wrapper = py_interface::effector_wrapper<hwlib::pin_out>(limo->heater);
        return wrapper;
    });

    m.def("getSyrupPump", [&](){
        static auto wrapper = py_interface::effector_wrapper<hwlib::pin_out>(limo->sirup_pump);
        return wrapper;
    });

    m.def("getSyrupValve", [&](){
        static auto wrapper = py_interface::effector_wrapper<hwlib::pin_out>(limo->sirup_valve);
        return wrapper;
    });

    m.def("getWaterPump", [&](){
        static auto wrapper = py_interface::effector_wrapper<hwlib::pin_out>(limo->water_pump);
        return wrapper;
    });

    m.def("getWaterValve", [&](){
        static auto wrapper = py_interface::effector_wrapper<hwlib::pin_out>(limo->water_valve);
        return wrapper;
    });

    m.def("getLedGreen", [&](){
        static auto wrapper = py_interface::effector_wrapper<hwlib::pin_out>(limo->led_green);
        return wrapper;
    });

    m.def("getLedYellow", [&](){
        static auto wrapper = py_interface::effector_wrapper<hwlib::pin_out>(limo->led_yellow);
        return wrapper;
    });

    m.def("openInterface", [&](int comNr, bool log_transactions = false, bool log_characters = false){
        limo = std::make_unique<lemonator_proxy>(comNr - 1, log_transactions, log_characters);
    });

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
