#ifndef AGRISEQ_KMER_ACCELERATOR_HPP
#define AGRISEQ_KMER_ACCELERATOR_HPP

#include <string>
#include <vector>
#include <cstdint>

namespace AgriSeq {

struct AlignStats {
    uint64_t total_reads;
    uint64_t matched_reads;
    double confidence_score;
};

class NativeEngine {
public:
    static AlignStats run_cuda_accelerated_match(const std::string& fastq_path);
};

} // namespace AgriSeq

#endif // AGRISEQ_KMER_ACCELERATOR_HPP
