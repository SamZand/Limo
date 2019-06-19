#ifdef PYBIND_DISABLED
#include <iostream>
#include <memory>

#include "lemonator_interface.hpp"
#include "lemonator_proxy.hpp"

std::unique_ptr<lemonator_proxy> limo;

int main() {
    int p = 3;

    std::cout << "Opening COM" << p << std::endl;
    limo = std::make_unique<lemonator_proxy>(p, 1, 1);
    std::cout << "New limo proxy at: " << (void*) limo.get() << std::endl;

    // auto color = limo->color.read_rgb();
    // std::cout << "Reading rgb (" << color.r << ", " << color.g << ", " << color.b << std::endl;
    
    auto distance = limo->distance.read_mm();
    std::cout << "Received distance: " << distance << std::endl;
}
#endif