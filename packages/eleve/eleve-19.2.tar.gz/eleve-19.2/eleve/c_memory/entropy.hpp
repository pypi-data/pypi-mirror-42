#ifndef _ENTROPY_HPP_
#define _ENTROPY_HPP_
#include "config.hpp"
#include <set>
#include <array>

struct HStats
{
    std::set<ID> terminals;
    
    struct Normalization
    {
        float mean;
        float stdev;
        COUNT count;
    };

    std::vector<Normalization> normalization;

    HStats(const std::set<ID> t): terminals(t) {};
    HStats() {};
};

#endif
