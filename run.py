import os

# def run_func(description, ppi_path, pseq_path, vec_path,
#             split_new, split_mode, train_valid_index_path,
#             use_lr_scheduler, save_path, graph_only_train, 
#             batch_size, epochs):
#     os.system("python -u gnn_train.py \
#             --description={} \
#             --ppi_path={} \
#             --pseq_path={} \
#             --vec_path={} \
#             --split_new={} \
#             --split_mode={} \
#             --gnn_model={} \
#             --use_lr_scheduler={} \
#             --save_path={} \
#             --graph_only_train={} \
#             --batch_size={} \
#             --epochs={} \
#             ".format(description, ppi_path, pseq_path, vec_path, 
#                     split_new, split_mode, train_valid_index_path,
#                     use_lr_scheduler, save_path, graph_only_train, 
#                     batch_size, epochs))

def run_func(description, ppi_path, pseq_path, vec_path,
            split_new, split_mode, train_valid_index_path, gnn_model,
            use_lr_scheduler, save_path, graph_only_train, 
            batch_size, epochs):
    os.system("python -u gnn_train.py \
            --description={} \
            --ppi_path={} \
            --pseq_path={} \
            --vec_path={} \
            --split_new={} \
            --split_mode={} \
            --train_valid_index_path={} \
            --gnn_model={}\
            --use_lr_scheduler={} \
            --save_path={} \
            --graph_only_train={} \
            --batch_size={} \
            --epochs={} \
            ".format(description, ppi_path, pseq_path, vec_path, 
                    split_new, split_mode, train_valid_index_path,gnn_model,
                    use_lr_scheduler, save_path, graph_only_train, 
                    batch_size, epochs))

if __name__ == "__main__":
    description = "test_string_bfs"

    # ppi_path = "./data/9606.protein.actions.all_connected.txt"
    # pseq_path = "./data/protein.STRING_all_connected.sequences.dictionary.tsv"
    # vec_path = "./data/vec5_CTC.txt"

    # ppi_path = "./data/4932.protein.actions.v11.0.txt"
    ppi_path = "./data/9606.protein.actions.all_connected.txt"
    # ppi_path = "./data/511145.protein.actions.v11.0.txt"

    # pseq_path = "./data/4932.protein.sequences.v11.0.tsv"
    pseq_path = "./data/protein.STRING_all_connected.sequences.dictionary.tsv"
    # pseq_path = "./data/511145.protein.sequences.v11.0.tsv"

    vec_path = "./data/vec5_CTC.txt"


    split_new = "True"
    split_mode = "random"
    # train_valid_index_path = "/content/drive/MyDrive/GNN_PPI/train_valid_index_json/string.bfs.fold1.json"
    train_valid_index_path = "/content/drive/MyDrive/GNN_PPI/train_valid_index_json/string.bfs.fold1_gat_homosapiens.json"

    # gnn_model = "./save_model/gnn_string_bfs/gnn_model_train.ckpt"
    # train_valid_index_path = "./save_model/gnn_string_bfs/gnn_model_train.ckpt"
    gnn_model = "./GCN_model/gnn_test_string_bfs_64/gnn_model_train.ckpt"

    use_lr_scheduler = "True"
    # save_path = "./save_model_fungus/"
    # save_path = "./save_model_new_fungus/"
    # save_path = "./save_model_bacteria/"
    # save_path = "./save_model/"
    # save_path = "./GCN_model_homosapiens/"
    # save_path = "./GCN_model_bacteri/"
    # save_path = "./GAT_model_fungus/"
    save_path = "./GAT_model_homosapiens/"




    graph_only_train = "True"

    batch_size = 2048
    epochs = 20
    # torch.cuda.empty_cache()
    run_func(description, ppi_path, pseq_path, vec_path, 
            split_new, split_mode, train_valid_index_path, gnn_model,
            use_lr_scheduler, save_path, graph_only_train, 
            batch_size, epochs)