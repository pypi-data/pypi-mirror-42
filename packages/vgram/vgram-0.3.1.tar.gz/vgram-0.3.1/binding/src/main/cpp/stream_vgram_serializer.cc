//
// Created by Aleksandr Khvorov on 11/02/2019.
//

#include <src/main/cpp/int_dict.h>
#include <fstream>
#include <iomanip>
#include <iostream>
#include "stream_vgram_serializer.h"

void StreamVgramSerializer::init_builder_fields_from_file(const std::string& filename, SeqCoder& coder,
                                                    std::vector<IntSeq>& seqs,  std::vector<IntSeq>& alphabet, IntSeq& freqs,
                                                    int& size, double& min_probability) const {
    std::ifstream file(filename);
    json dict;
    file >> dict;
    file.close();
    size = dict["size"];
    min_probability = dict["min_prob"];
    for (int n : dict["coder"]) {
        alphabet.emplace_back(1, n);
        coder.encode(std::vector<int>(1, n));
    }
    for (const auto &word_obj : dict["alphabet"]) {
        freqs.push_back(word_obj["freq"].get<int>());
        seqs.push_back(word_obj["vec"].get<IntSeq>());
    }
}

void StreamVgramSerializer::write_to_file(const std::string& filename, const std::string& default_filename,
                                    BaseTokenizer* tokenizer, int size, double min_probability) const {
    std::ofstream file;
    if (filename.empty() && !default_filename.empty()) {
        file = std::ofstream(default_filename);
    } else if (!filename.empty()) {
        file = std::ofstream(filename);
    } else {
        std::cout << "Error: no filename for save. Pass filename to constructor or save method" << std::endl;
    }
    file << std::setw(2) << dict_to_json(tokenizer, size, min_probability) << std::endl;
    file.close();
}

json StreamVgramSerializer::dict_to_json(BaseTokenizer* tokenizer) const {
    json dict;
    dict["size"] = size_;
    dict["min_prob"] = min_probability_;
    dict["coder"] = coder_to_json(coder_);
    dict["alphabet"] = alphabet_to_json(dict_, freqs_, coder_, tokenizer);
    return dict;
}

json StreamVgramSerializer::coder_to_json(const SeqCoder& coder) const {
    std::vector<std::pair<int, int>> pairs;
    for (const auto& p : coder.code_map()) {
        pairs.emplace_back(p);
    }
    std::sort(pairs.begin(), pairs.end(), [](const std::pair<int,int>& a, const std::pair<int,int>& b) { return a.second < b.second; });
    std::string res;
    json coder_json;
    for (const auto& p : pairs) {
        coder_json.push_back(p.first);
    }
    return coder_json;
}

json StreamVgramSerializer::alphabet_to_json(const std::shared_ptr<IntDict>& dict, const IntSeq& freqs, const SeqCoder& coder,
                                       BaseTokenizer* tokenizer) const {
    json alpha;
    for (int i = 0; i < dict->alphabet().size(); i++) {
        auto word = dict->alphabet()[i];
        json word_obj;
        word_obj["vec"] = json(word);
        word_obj["freq"] = freqs[i];
        if (tokenizer != nullptr)
            word_obj["text"] = tokenizer->decode(std::vector<std::vector<int>>(1, coder.decode(dict->get(i))))[0];
        alpha.push_back(word_obj);
    }
    return alpha;
}
