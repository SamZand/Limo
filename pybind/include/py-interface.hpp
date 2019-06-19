#pragma once

#include <pybind11/pybind11.h>
#include <iostream>
#include <memory>

namespace py = pybind11;

#include "lemonator_interface.hpp"
#include "lemonator_proxy.hpp"

std::unique_ptr<lemonator_proxy> limo;

PYBIND11_MODULE(lemonator, m) {
/*
 *  Reference python implementation of LemonatorInterface
 * 
 *  class LemonatorInterface:
 *      def __init__(self, effectors, sensors):
 *        self.lcd = effectors['lcd']
 *        self.keypad = sensors['keypad']
 *
 *          self.distance = sensors['level']
 *          self.colour = sensors['colour']
 *          self.temperature = sensors['temp']
 *          self.presence = sensors['presence']
 *
 *          self.heater = effectors['heater']
 *          self.syrup_pump = effectors['pumpB']
 *          self.syrup_valve = effectors['valveB']
 *          self.water_pump = effectors['pumpA']
 *          self.water_valve = effectors['valveA']
 *          self.led_green = effectors['greenM']
 *          self.led_yellow = effectors['yellowM']
 *
 *          # TODO: Define
 *          self.syrup = None
 *          self.water = None
 */

    m.def("open_port", [&](int p) {
        std::cout << "Opening COM" << p << std::endl;
        limo = std::make_unique<lemonator_proxy>(p, 1, 1);
        std::cout << "New limo proxy at: " << (void*) limo.get() << std::endl;
    });

    m.def("toggle_led", [&]() {
        static bool i = false;
        std::cout << "Using limo: " << (void*) limo.get() << std::endl;
        limo->led_green.write(!i);
    });
    
    m.def("write_serial", [&](const std::string &s) {
        std::cout << "Writing to lcd: \"" << s << '\"' << std::endl;
        limo->lcd << s.c_str();
    });

    m.def("read_rgb", [&]() {
        std::cout << "Reading rgb (" << std::flush;
        auto color = limo->color.read_rgb();
        std::cout << color.r << ", " << color.g << ", " << color.b << std::endl;
    });

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
