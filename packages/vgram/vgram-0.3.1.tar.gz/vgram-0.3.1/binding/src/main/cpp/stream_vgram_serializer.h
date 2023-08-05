//
// Created by Aleksandr Khvorov on 11/02/2019.
//

#ifndef DICT_EXPANSION_STREAM_VGRAM_SERIALIZER_H
#define DICT_EXPANSION_STREAM_VGRAM_SERIALIZER_H


#include "json.h"
#include "base_tokenizer.h"
#include <src/main/cpp/int_dict.h>
#include <src/main/cpp/seq_coder.h>

using json = nlohmann::json;

class StreamVgramSerializer {
public:
    void init_builder_fields_from_file(const std::string& filename, SeqCoder& coder, std::vector<IntSeq>& seqs,
                                       std::vector<IntSeq>& alphabet, IntSeq& freqs,
                                       int& size, double& min_probability) const;
    void write_to_file(const std::string& filename, const std::string& default_filename,
                       BaseTokenizer* tokenizer, int size, double min_probability) const;
    json dict_to_json(BaseTokenizer* tokenizer) const;
    json alphabet_to_json(const std::shared_ptr<IntDict>& dict, const IntSeq& freqs, const SeqCoder& coder,
                          BaseTokenizer* tokenizer) const;
    json coder_to_json(const SeqCoder& coder) const;
//    json read_dict(const std::string& filename) const;
};


#endif //DICT_EXPANSION_STREAM_VGRAM_SERIALIZER_H
