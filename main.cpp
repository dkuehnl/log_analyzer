#include <iostream>
#include <algorithm>
#include <string>
#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/embed.h>
#include <pybind11/stl.h>

namespace py = pybind11;

int main() {

    py::scoped_interpreter guard{};
    py::module_ log_parser = py::module_::import("parse_log"); 
    py::object parse_logfile = log_parser.attr("parse_logfile"); 

    std::string logfile = "/home/dkuehnlein/workspace/cpp/python-cpp/IMS.log_20250409085500.log";
    auto data = parse_logfile(logfile).cast<std::vector<std::vector<std::string>>>(); 

/*    std::sort(data.begin(), data.end(), 
        [](auto &a, auto &b) {
            return a[0]<b[0];
        });
*/
    for (int line = 0; line < data.size(); line++) {
        std::cout << line << ": ";
        for (int element = 0; element < data[line].size(); element++) {
            std::cout << data[line][element] << " ";
        }
        std::cout << std::endl; 
        if (line > 100) {
            break; 
        }
    }


    return 0; 
}
/*int main() {
    py::scoped_interpreter guard{};
    py::module_ add_mod = py::module_::import("add"); 

    py::object add_func = add_mod.attr("add_number");

    // Beispielaufrufe mit verschiedenen Typen
    int x = 5, y = 7;
    auto result = add_func(x, y).cast<int>();  // cast zurück zu int

    std::cout << "add_number(" << x << ", " << y << ") = " << result << std::endl;

    // Du könntest auch floats oder andere Typen probieren:
    double a = 2.5, b = 4.75;
    double res2 = add_func(a, b).cast<double>();
    std::cout << "add_number(" << a << ", " << b << ") = " << res2 << std::endl;

    return 0;
}*/