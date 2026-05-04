import requests
import json

URL = "https://api.platform.opentargets.org/api/v4/graphql"

def get_disease_subtypes(disease_id):
    """Returns a list of immediate child diseases (subtypes)."""
    formatted_id = disease_id.replace(":", "_")
    query = """
    query DiseaseSubtypes($id: String!) {
      disease(efoId: $id) {
        children {
          id
          name
        }
      }
    }
    """
    variables = {"id": formatted_id}
    response = requests.post(URL, json={'query': query, 'variables': variables})
    data = response.json()
    disease_node = data.get('data', {}).get('disease')
    return disease_node.get('children', []) if disease_node else []

def get_msi_data(disease_id):
    """Returns clinical drug candidates and their mechanisms for a specific disease."""
    formatted_id = disease_id.replace(":", "_")
    query = """
    query DiseaseMsiData($id: String!) {
      disease(efoId: $id) {
        id
        name
        dbXRefs
        drugAndClinicalCandidates {
          rows {
            drug {
              id
              name
              crossReferences {
                source
                ids
              }
              mechanismsOfAction {
                rows {
                  targets {
                    id
                    approvedSymbol
                  }
                }
              }
            }
          }
        }
      }
    }
    """
    variables = {"id": formatted_id}
    response = requests.post(URL, json={'query': query, 'variables': variables})
    return response.json()

def extract_msi_records(data):
    """Parses OpenTargets response into MSI formatted nested dictionary."""
    if not data.get("data") or not data["data"].get("disease"):
        return None
    
    disease_node = data["data"]["disease"]
    
    # Extract UMLS ID (Stripping 'UMLS:' prefix)
    umls_ids = [i.split(":")[1] for i in disease_node.get("dbXRefs", []) if i.startswith("UMLS")]
    if not umls_ids:
        return None
    
    primary_umls = umls_ids[0]
    drug_info = {}

    for row in disease_node.get('drugAndClinicalCandidates', {}).get('rows', []):
        drug_entry = row.get("drug")
        if not drug_entry:
            continue
            
        # Get DrugBank ID
        db_ids = [ref['ids'] for ref in drug_entry.get('crossReferences', []) if ref["source"] == 'drugbank']
        if not db_ids or not db_ids[0]:
            continue
            
        primary_dbid = db_ids[0][0]
        
        # Collect Targets (Gene Symbols)
        target_symbols = []
        if drug_entry.get('mechanismsOfAction'):
            for mech in drug_entry['mechanismsOfAction'].get('rows', []):
                for target in mech.get('targets', []):
                    symbol = target.get('approvedSymbol')
                    if symbol:
                        target_symbols.append(symbol)
        
        drug_info[primary_dbid] = {
            "drug_name": drug_entry["name"],
            "target_gene_symbols": list(set(target_symbols))
        }

    return {
        "umls_id": primary_umls,
        "disease_name": disease_node["name"],
        "drugs": drug_info
    }
