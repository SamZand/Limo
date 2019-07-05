#ifdef PYBIND_DISABLED
#include <iostream>
#include <memory>

#include "lemonator_interface.hpp"
#include "lemonator_proxy.hpp"

std::unique_ptr<lemonator_proxy> limo;

int main() {

}
#else
#include "py-interface.hpp"
#endif