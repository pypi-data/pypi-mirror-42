#ifndef HGMeans_H
#define HGMeans_H

/* Authors: Daniel Gribel and Thibaut Vidal
 * Contact: dgribel@inf.puc-rio.br
 *
 */

#include "GeneticOperations.h"
#include <fstream>
#include <sstream>
#include <iomanip>
#include <ctime>

#define SAVE_FILE true

class HGMeans {
    public:
        HGMeans();
        ~HGMeans();
        void Go(char* filename, int size_population, int it, bool evaluation, const std::vector<int>& m); 
};

class InputValidator {
    
    private:

        int nb_arg;

        string dataset_path;

        string dataset_name;

        int pi_min;

        int max_it;

        bool external_eval;

        vector<int> nb_clusters;

    public:

        InputValidator(int argc, char* argv[]) {

            nb_arg = argc; 

            if(nb_arg >= 6) {
                // Dataset path
                dataset_path = argv[1];

                // Population size (Pi_min paramter)
                pi_min = atoi(argv[2]);

                // Maxixum number of iterations parameter
                max_it = atoi(argv[3]);

                // External clustering evaluation parameter
                external_eval = atoi(argv[4]);

                for(int i = 5; i < argc; i++) {
                    nb_clusters.push_back(atoi(argv[i]));
                }
                if (dataset_path.find(DATA_PATH) != string::npos &&
                    dataset_path.find(".txt") != string::npos) {
                    dataset_name = ReplaceString(dataset_path, DATA_PATH, "");
                    dataset_name = ReplaceString(dataset_name, ".txt", "");
                }
            }
        }

        InputValidator(std::string filename, int size_population, int it, bool evaluation, std::vector<int> m) {

            nb_arg = 6; 

            // Dataset path
            dataset_path = filename;

            // Population size (Pi_min paramter)
            pi_min = size_population;

            // Maxixum number of iterations parameter
            max_it = it;

            // External clustering evaluation parameter
            external_eval = evaluation;

            nb_clusters = m;
            
            if (dataset_path.find(DATA_PATH) != string::npos &&
                dataset_path.find(".txt") != string::npos) {
                dataset_name = ReplaceString(dataset_path, DATA_PATH, "");
                dataset_name = ReplaceString(dataset_name, ".txt", "");
            }
        }

        string GetDatasetPath() { return dataset_path; };

        string GetDatasetName() { return dataset_name; };

        int GetPiMin() { return pi_min; };

        int GetMaxIt() { return max_it; };

        bool ExternalEval() { return external_eval; };

        vector<int> GetNbClusters() { return nb_clusters; };

        bool Validate() {

            // At least 6 parameters should be provided:
            // Program name, dataset, size of population, maximum iterations, evaluation and number of clusters
            if(nb_arg < 6) {
                cerr << "Insufficient number of parameters provided. Please use the following input format:" << 
                endl << "./hgmeans DatasetPath Pi_min N2 Evaluate [M]" << endl;
                return false;
            }
            
            ifstream input(dataset_path.c_str());

            if (!input) {
                cerr << "Unable to open data file: " << dataset_path << endl;
                return false;
            }

            // Checking bounds of variables
            if(pi_min < 1 || pi_min > 100000) {
                cerr << "Pi_min out of bounds" << endl;
                return false;
            }
            
            if(max_it < 1 || max_it > 100000) {
                cerr << "Max_it out of bounds" << endl;
                return false;
            }

            if(external_eval != 0 && external_eval != 1) {
                cerr << "Incorrect value for evaluation" << endl;
                return false;
            }
                
            for(int i = 0; i < nb_clusters.size(); i++) {
                if(nb_clusters[i] < 1 || nb_clusters[i] > USHRT_MAX) { // Range for m must be [1, 65535]
                    cerr << "The number of clusters is out of the limit [1, " << USHRT_MAX << "]" << endl;
                    return false;
                }
            }
            return true;
        }
};

#endif