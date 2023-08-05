//
// Created by Aleksandr Khvorov on 11/02/2019.
//

#ifndef DICT_EXPANSION_VGRAM_SERIALIZER_H
#define DICT_EXPANSION_VGRAM_SERIALIZER_H

#include <fstream>
#include "json.h"
#include "base_tokenizer.h"
#include <src/main/cpp/int_dict.h>
#include <src/main/cpp/seq_coder.h>

using json = nlohmann::json;

class VgramSerializer {
public:
    static void init_builder_fields_from_file(const std::string& filename, SeqCoder& coder,
                                                               std::vector<IntSeq>& seqs,  std::vector<IntSeq>& alphabet, IntSeq& freqs,
                                                               int& size, double& min_probability) {
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

    static json coder_to_json(const SeqCoder& coder) {
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

    static json alphabet_to_json(const std::shared_ptr<IntDict>& dict, const IntSeq& freqs, const SeqCoder& coder,
                                                  BaseTokenizer* tokenizer) {
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
};


#endif //DICT_EXPANSION_VGRAM_SERIALIZER_H
