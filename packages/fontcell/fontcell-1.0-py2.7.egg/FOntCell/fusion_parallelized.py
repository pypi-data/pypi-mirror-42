# Libraries #
import os
from . import ontology_fusion as of
from mpi4py import MPI
from . import doc_managing as doc
# ######### #

def read_variables(variable):
    try:
        vari = eval(variable)
    except:
        vari = variable
    return vari

# Read the configurations
def import_and_delete():
    root_dir = os.path.dirname(os.path.realpath(__file__))
    proyect_path = os.path.abspath(os.path.join(root_dir, os.pardir))
    r_path = proyect_path + os.sep + 'files' + os.sep
    list_of_variables = doc.import_txt(r_path + 'parallelization_config.txt')
    ontology1 = doc.import_csv(r_path + 'onto1_for_parallel.csv')
    ontology2 = doc.import_csv(r_path + 'onto2_for_parallel.csv')

    onto_name1 = read_variables(list_of_variables[0])
    onto_name2 = read_variables(list_of_variables[1])
    file1 = read_variables(list_of_variables[2])
    onto1_fuseclasses = read_variables(list_of_variables[3])
    onto2_fuseclasses = read_variables(list_of_variables[4])
    onto1_restriction = read_variables(list_of_variables[5])
    onto2_restriction = read_variables(list_of_variables[6])
    onto1_list_clear = read_variables(list_of_variables[7])
    onto2_list_clear = read_variables(list_of_variables[8])
    synonyms = read_variables(list_of_variables[9])
    text_process = read_variables(list_of_variables[10])
    split_from1 = read_variables(list_of_variables[11])
    split_since1 = read_variables(list_of_variables[12])
    split_from2 = read_variables(list_of_variables[13])
    split_since2 = read_variables(list_of_variables[14])
    windowsize = read_variables(list_of_variables[15])
    globalthreshold = read_variables(list_of_variables[16])
    localthreshold = read_variables(list_of_variables[17])
    save_internals = read_variables(list_of_variables[18])
    parallelization = True
    OBO_format_result = read_variables(list_of_variables[20])
    save_internals_equiv = read_variables(list_of_variables[21])
    folder = read_variables(list_of_variables[22])
    draw_circular = read_variables(list_of_variables[23])
    topological_test = read_variables(list_of_variables[24])
    constriction_threshold = read_variables(list_of_variables[25])
    topological_cosine = read_variables(list_of_variables[26])
    topological_pearson = read_variables(list_of_variables[27])
    topological_euclidean = read_variables(list_of_variables[28])
    topological_threshold = read_variables(list_of_variables[29])
    root = read_variables(list_of_variables[30])

    return ontology1, ontology2, onto_name1, onto_name2, file1,onto1_fuseclasses, onto2_fuseclasses\
        , onto1_restriction, onto2_restriction, onto1_list_clear, onto2_list_clear, synonyms\
        , text_process, split_from1, split_since1, split_from2, split_since2, windowsize\
        , globalthreshold, localthreshold, save_internals, parallelization, OBO_format_result\
        , save_internals_equiv, folder, draw_circular, topological_test, constriction_threshold, topological_cosine\
        , topological_pearson, topological_euclidean, topological_threshold, root


# Perform the fusion parallelizing
def ontology_fusion_parallelized():
    ontology1, ontology2, onto_name1, onto_name2, file1, onto1_fuseclasses, onto2_fuseclasses\
        , onto1_restriction, onto2_restriction, onto1_list_clear, onto2_list_clear, synonyms\
        , text_process, split_from1, split_since1, split_from2, split_since2, windowsize\
        , globalthreshold, localthreshold, save_internals, parallelization, OBO_format_result\
        , save_internals_equiv, folder, draw_circular, topological_test, constriction_threshold, topological_cosine\
        , topological_pearson, topological_euclidean, topological_threshold, root = import_and_delete()

    of.fuseOntologies3(ontology1, ontology2, onto_name1, onto_name2, onto1_path=file1,
                       onto1_fuseclasses=onto1_fuseclasses, onto2_fuseclasses=onto2_fuseclasses,
                       onto1_restriction=onto1_restriction, onto2_restriction=onto2_restriction,
                       onto1_list_clear=onto1_list_clear, onto2_list_clear=onto2_list_clear, synonyms=synonyms,
                       text_process=text_process, split_from1=split_from1, split_since1=split_since1,
                       split_from2=split_from2, split_since2=split_since2, windowsize=windowsize,
                       globalthreshold=globalthreshold, localthreshold=localthreshold,
                       constriction_threshold=constriction_threshold, topological_threshold=topological_threshold,
                       save_internals=save_internals, parallelization=parallelization,
                       OBO_format_result=OBO_format_result, save_internals_equiv=save_internals_equiv,
                       draw_circular=draw_circular, topological_test=topological_test,
                       topological_cosine=topological_cosine, topological_pearson=topological_pearson,
                       topological_euclidean=topological_euclidean)
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    if rank == 0:
        root_dir = os.path.dirname(os.path.realpath(__file__))
        proyect_path = os.path.abspath(os.path.join(root_dir, os.pardir))
        current_path = os.path.dirname(os.path.realpath(__file__)) + os.sep
        os.remove(current_path + 'parallelization_config.txt')
        os.remove(current_path + 'onto1_for_parallel.csv')
        os.remove(current_path + 'onto2_for_parallel.csv')
        os.remove(current_path + 'graph.gv')
        os.remove(current_path + 'graph.gv.pdf')
        os.remove(current_path + 'graph.gv.plain')
        os.remove(proyect_path + os.sep + 'files' + os.sep + 'graph_viz_coord.ods')
    return


if __name__ == '__main__':
    ontology_fusion_parallelized()
