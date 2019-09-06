import sys


def AddPwyName(pwy_list, pwynames_dict):

    pwy_translate_list = []

    if pwy_list == None:
         pwy_translate_list.append('None')
    else:
        for i in pwy_list:
            pwy_trns = i + ':' + str(pwynames_dict.get(i))
            pwy_translate_list.append(pwy_trns)
            
    pwy_trns_str  =  "\t".join(pwy_translate_list) 
    
    return pwy_trns_str
            



    
def bigg2dict(big_file):
    
   
    
    bigg_dict = {}


    for line in big_file:
        line_list = line.strip().split('\t')
        link_bigg_list = line_list[4].split(';')
        bigg_code = line_list[0]
    
        if link_bigg_list[0].startswith('MetaNetX'):
            mtnx_code = link_bigg_list[0].split('/')[-1]
            bigg_dict[bigg_code] = mtnx_code
        else:
            for i in link_bigg_list:
                link = i.strip().replace(' ', '')
                if link.startswith('MetaNetX'):
                    mtnx_code = link.split('/')[-1]
                    bigg_dict[bigg_code] = mtnx_code


    return bigg_dict 


def metanetx2dict(metanetx_db):
    
    dict_metanetx = {}

    for i in metanetx_db:
        if i.startswith('#'):
            pass
        
        else:
        
            if i.startswith('metacyc'):
        
                MNX_DICT = i.strip().split("\t")[1]
                
                XREF_DICT = i.strip().split("\t")[0]
            
                
                XREF_DICT2 = XREF_DICT.replace('metacyc:','', 1)
                
        
                if dict_metanetx.get(MNX_DICT) is None:
                    dict_metanetx[MNX_DICT]=[XREF_DICT2]
                else:
                    dict_metanetx[MNX_DICT].append(XREF_DICT2)

                
    return dict_metanetx




def metacyc2dict(metacyc_db):
    
    reacciones_file = []
    aux = []
    for i in metacyc_db:
        pattern_line = i.strip()
        if pattern_line.startswith('#'):
            pass
        else:
            if pattern_line == '//' and len(aux) != 0:
                reacciones_file.append(aux)
                aux = []
                aux.append(pattern_line)
            else:
                aux.append(pattern_line)
    reacciones_file.append(aux)



    metacyc_dict = {}
    rxn_list = []

    reacciones_file.pop(-1) # delete the last element --> '//'

    for i in reacciones_file:
        tmp_list = []
        for l in i:
            reaccion_value = l.strip()
            if reaccion_value.startswith('UNIQUE-ID'):
                reaccion_value_list = reaccion_value.strip().split(' ')
                rxn_names = " ".join(reaccion_value_list[2:])
                tmp_list.append(rxn_names)
            elif reaccion_value.startswith('IN-PATHWAY'):
                pwy_value_list = reaccion_value.strip().split()
                pwy_names = ' '.join(pwy_value_list[2:])
                tmp_list.append(pwy_names)
        rxn_list.append(tmp_list)
    

    for i in rxn_list:
        rxn_id = i[0]
        rxn_pwy = i[1:] 
        metacyc_dict[rxn_id] = rxn_pwy
    
    return metacyc_dict
    


def pwynames2dict(pwynames_db):
    
    reacciones_file = []
    aux = []
    for i in pwynames_db:
        pattern_line = i.strip()
        if pattern_line.startswith('#'):
            pass
        else:
            if pattern_line == '//' and len(aux) != 0:
                reacciones_file.append(aux)
                aux = []
                aux.append(pattern_line)
            else:
                aux.append(pattern_line)
    reacciones_file.append(aux)


    pwynames_dict = {}

            
    rxn_list = []

    for i in reacciones_file:
        tmp_list = []
        for l in i:
            reaccion_value = l.strip()
            if reaccion_value.startswith('UNIQUE-ID'):
                tmp_variable = " ".join(reaccion_value.strip().split()[2:])
                tmp_list.append(tmp_variable)
            elif reaccion_value.startswith('COMMON-NAME'):
                tmp_variable2 = " ".join(reaccion_value.strip().split()[2:])
                tmp_list.append(tmp_variable2)
        rxn_list.append(tmp_list)
    

    for i in rxn_list:
        try:
            rxn_id = i[0]
            rxn_pwy = i[1:] 
            pwynames_dict[rxn_id] = rxn_pwy
        except IndexError:
            pass
        
    return pwynames_dict

    


    
def read_dict(dict_bigg, dict_metanetx, metacyc_dict, pwynames_dict, bigg_id):



    output_dict = {}
    
    for key, value in dict_bigg.iteritems():
        rxn_metacyc = dict_metanetx.get(value)

        if rxn_metacyc is None:
            output_dict[key] = [value, rxn_metacyc]

        else:
            for i in rxn_metacyc:
                pwy_rxn = metacyc_dict.get(i)
                output_dict[key] = [value, i, AddPwyName(pwy_rxn, pwynames_dict)] 
    
    
    
    for k, v in output_dict.iteritems():
        if k == bigg_id:
            print k
            
            if v[1] is None:
                print '*No hay vias metacyc asociadas*' 
                    
            else: 
                for m in v[1].split():
                    print m
                for l in v[2].split('\t'):
                    print l


def main():
    big_file = open('bigg_models_reactions.txt', 'r')
    # bigg_db = open('./datos-bigg.txt', 'r')
    metanetx_db = open('./datos-metanetx.tsv', 'r')
    metacyc_db = open('./reactions.dat', 'r')
    pwynames_db = open('./pathways.dat', 'r')
    bigg_id = sys.argv[1]
    
    dict_bigg = bigg2dict(big_file)
    dict_metanetx = metanetx2dict(metanetx_db)
    metacyc_dict = metacyc2dict(metacyc_db)
    pwynames_dict = pwynames2dict(pwynames_db)

    
    read_dict(dict_bigg, dict_metanetx, metacyc_dict, pwynames_dict, bigg_id)
    

 
        

if __name__ == "__main__":
    main()