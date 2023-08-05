//
// Created by Aleksandr Khvorov on 03/11/2018.
//

#include <algorithm>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <src/main/cpp/int_dict_p.h>
#include <src/main/cpp/int_vgram_builder_p.h>
#include "py_stream_vgram_builder.h"
#include "vgram_serializer.h"

PyStreamVGramBuilder::PyStreamVGramBuilder(int size) : PyStreamVGramBuilder(size, 1) {}

PyStreamVGramBuilder::PyStreamVGramBuilder(int size, int verbose) : PyStreamVGramBuilder(size, "", verbose) {}

PyStreamVGramBuilder::PyStreamVGramBuilder(int size, const std::string& filename)
: PyStreamVGramBuilder(size, filename, 1) {}

PyStreamVGramBuilder::PyStreamVGramBuilder(int size, const std::string& filename, int verbose) {
    builder_ = std::shared_ptr<IntVGramBuilder>(new IntVGramBuilderImpl(size - 1, verbose));
    size_ = size;
    dict_ = nullptr;
    coder_ = SeqCoder();
    freqs_ = IntSeq();
    total_freqs_ = 0;
    verbose_ = verbose;
    filename_ = filename;
}

PyStreamVGramBuilder::PyStreamVGramBuilder(const std::string& filename) : PyStreamVGramBuilder(filename, 1) {}

PyStreamVGramBuilder::PyStreamVGramBuilder(const std::string& filename, int verbose) {
    coder_ = SeqCoder();
    std::vector<IntSeq> seqs, alphabet;
    VgramSerializer::init_builder_fields_from_file(filename, coder_, seqs, alphabet, freqs_, size_, min_probability_);
    total_freqs_ = std::accumulate(freqs_.begin(), freqs_.end(), 0);
    dict_ = std::shared_ptr<IntDict>(new IntDictImpl(seqs));
    builder_ = std::shared_ptr<IntVGramBuilder>(new IntVGramBuilderImpl(*dict_, freqs_, alphabet, min_probability_, verbose));
    verbose_ = verbose;
}

void PyStreamVGramBuilder::accept(const IntSeq& seq) {
    builder_->accept(coder_.encode(seq));
}

IntSeq PyStreamVGramBuilder::parse(const IntSeq& seq) const {
    IntSeq result;
    dict_->parse(coder_.encode_immutable(seq), freqs_, total_freqs_, &result);
    return result;
}

void PyStreamVGramBuilder::update_dict() {
    if (dict_ != builder_->result()) {
        dict_ = builder_->result();
        builder_->result_freqs(&freqs_);
        total_freqs_ = std::accumulate(freqs_.begin(), freqs_.end(), 0);
        min_probability_ = builder_->get_min_probability();
    }
}

void PyStreamVGramBuilder::save(const std::string& filename, BaseTokenizer* tokenizer) const {
//    VgramSerializer().write_to_file(filename, filename_, tokenizer, size_, min_probability_);
    std::ofstream file;
    if (filename.empty() && !filename_.empty()) {
        file = std::ofstream(filename_);
    } else if (!filename.empty()) {
        file = std::ofstream(filename);
    } else {
        std::cout << "Error: no filename for save. Pass filename to constructor or save method" << std::endl;
    }
    file << std::setw(2) << dict_to_json(tokenizer) << std::endl;
    file.close();
}

json PyStreamVGramBuilder::dict_to_json(BaseTokenizer* tokenizer) const {
    json dict;
    dict["size"] = size_;
    dict["min_prob"] = min_probability_;
    dict["coder"] = VgramSerializer::coder_to_json(coder_);
    dict["alphabet"] = VgramSerializer::alphabet_to_json(dict_, freqs_, coder_, tokenizer);
    return dict;
}

json PyStreamVGramBuilder::read_dict(const std::string& filename) {
    std::ifstream file(filename);
    json dict;
    file >> dict;
    file.close();
    return dict;
}

std::vector<IntSeq> PyStreamVGramBuilder::alphabet() const {
    std::vector<IntSeq> alpha;
    for (const auto &a : dict_->alphabet()) {
        alpha.push_back(coder_.decode(a));
    }
    return alpha;
}

IntSeq PyStreamVGramBuilder::freqs() const {
    return freqs_;
}
