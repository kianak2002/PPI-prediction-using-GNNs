import os


def run_func(description, ppi_path, pseq_path, vec_path,
            index_path, gnn_model, test_all):
    os.system("python gnn_test.py \
            --description={} \
            --ppi_path={} \
            --pseq_path={} \
            --vec_path={} \
            --index_path={} \
            --gnn_model={} \
            --test_all={} \
            ".format(description, ppi_path, pseq_path, vec_path, 
                    index_path, gnn_model, test_all))

if __name__ == "__main__":
    description = "test"

    # ppi_path = "./data/9606.protein.actions.all_connected.txt"
    ppi_path = "./data/4932.protein.actions.v11.0.txt"
    # ppi_path = "./data/511145.protein.actions.v11.0.txt"

    # pseq_path = "./data/protein.STRING_all_connected.sequences.dictionary.tsv"
    pseq_path = "./data/4932.protein.sequences.v11.0.tsv"
    # pseq_path = "./data/511145.protein.sequences.v11.0.tsv"

    vec_path = "./data/vec5_CTC.txt"

    # index_path = "./train_valid_index_json/string.bfs.fold1.json"
    # index_path = "./train_valid_index_json/string.bfs.fold1_bacteri.json"
    # index_path = "./train_valid_index_json/string.bfs.fold1_gcn_fungus.json"
    # index_path = "./train_valid_index_json/string.bfs.fold1_gat_homosapiens.json"
    # index_path = "./train_valid_index_json/string.bfs.fold1_gat_fungus.json"
    # index_path = "./train_valid_index_json/string.bfs.fold1_gat_bacteri.json"
    # index_path = "./train_valid_index_json/string.bfs.fold1_gat_homosapiens.json"
    # index_path = "./train_valid_index_json/string.bfs.fold1_gcn_homosapiens.json"
    index_path = "./train_valid_index_json/string.bfs.fold1_gcn_bacteri.json"



    # gnn_model = "./save_model/gnn_string_bfs/gnn_model_train.ckpt"
    # gnn_model = "./save_model_new_fungus/gnn_test_string_bfs/gnn_model_train.ckpt"
    # gnn_model = "./GCN_model_homosapiens/gnn_test_string_bfs_8/gnn_model_train.ckpt"
    gnn_model = "./GCN_model_bacteri/gnn_test_string_bfs_8/gnn_model_train.ckpt"
    # gnn_model = "./GAT_model_fungus/gnn_test_string_bfs_16/gnn_model_train.ckpt"
    # gnn_model = "./GAT_model_homosapiens/gnn_test_string_bfs_8/gnn_model_train.ckpt"
    # gnn_model = "./save_model_bacteria/gnn_test_string_bfs/gnn_model_train.ckpt"
    # gnn_model = "./GCN_model_fungus/gnn_test_string_bfs_64/gnn_model_train.ckpt"
    # gnn_model = "./GAT_model_bacteri/gnn_test_string_bfs_8/gnn_model_train.ckpt"

    test_all = "False"

    # test test

    run_func(description, ppi_path, pseq_path, vec_path, index_path, gnn_model, test_all)
