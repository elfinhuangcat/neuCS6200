package classifier;

import data_preprocess.FillMissingValue;
import data_preprocess.MyResampler;
import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.classifiers.bayes.NaiveBayes;
import weka.classifiers.functions.Logistic;
import weka.classifiers.lazy.IBk;
import weka.classifiers.meta.Bagging;
import weka.classifiers.trees.J48;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;




/**
 * Created by jalpanranderi on 4/28/15.
 */
public class KNN_Bag {

    public Classifier model;
    public int k;

    public KNN_Bag() {
    }


    public KNN_Bag(Classifier model) {
        this.model = model;
    }


    public void train(Instances traindata) throws Exception {
        if(model == null){
            IBk knn = new IBk();
            knn.setKNN(1);
            model = knn;
        }
        model.buildClassifier(traindata);
    }

    public double getClass(Instance test_instance) throws Exception {
        return model.classifyInstance(test_instance);
    }

    public static void main(String[] args) throws Exception {
        if(args.length != 2){
            System.out.println("Usage :  train.arff test.arff");
            System.exit(0);
        }
//        run(args);
        // 1. Add Missing values
        DataSource train = new DataSource(args[0]);
        Instances trainingSet = train.getDataSet();
        trainingSet.setClassIndex(trainingSet.numAttributes() - 1);
        trainingSet = FillMissingValue.fillMissingValues(trainingSet);




        // 2. Balance data
        trainingSet = MyResampler.resampleToBalance(trainingSet);

        // 3. Bagging
//        Bagging bag = new Bagging();
//        bag.setClassifier(new IBk());
//        bag.buildClassifier(trainingSet);

        Bagging nbBag = new Bagging();
        nbBag.setClassifier(new NaiveBayes());
        nbBag.buildClassifier(trainingSet);

        Bagging lrBag = new Bagging();
        lrBag.setClassifier(new Logistic());
        lrBag.buildClassifier(trainingSet);

        Bagging treeBag = new Bagging();
        treeBag.setClassifier(new J48());
        treeBag.buildClassifier(trainingSet);



        // 4. Error Testing
        DataSource test = new DataSource(args[1]);
        Instances testingSet = test.getDataSet();
        testingSet.setClassIndex(testingSet.numAttributes() - 1);

        System.out.println("\nBagging Results ");

        // knn test
        Evaluation eval = new Evaluation(trainingSet);
//        eval.evaluateModel(bag, testingSet);
////        System.out.println(model.toString());
//        System.out.println("Knn " + eval.errorRate());


        // naive bayes test
        eval.evaluateModel(nbBag, testingSet);
//        System.out.println(model.toString());
        System.out.println("Naive Bayes " + eval.errorRate());



        // logistic regression test
        eval.evaluateModel(lrBag, testingSet);
//        System.out.println(model.toString());
        System.out.println("Logistic Regression " + eval.errorRate());


        // descion tree test
        eval.evaluateModel(treeBag, testingSet);
//        System.out.println(model.toString());
        System.out.println("Descion Tree " + eval.errorRate());




//        System.out.println("======\nConfusion Matrix:");
//
//        printMatrix(eval.confusionMatrix());

        System.out.println("Error rate: "+eval.errorRate());

    }



    /**
     * -0 train.arff
     * -1 test.arff
     *
     * @param args
     * @return
     */
    public static double run(String[] args) throws Exception {

        // 1. Read training file
        DataSource train = new DataSource(args[0]);
        Instances trainingSet = train.getDataSet();
        trainingSet.setClassIndex(trainingSet.numAttributes() - 1);


        // 2. filling the missing value
        trainingSet = FillMissingValue.fillMissingValues(trainingSet);


        // 3. Balance dataset
        trainingSet = MyResampler.resampleToBalance(trainingSet);


        // 4. Train
        IBk knn = new IBk();
        knn.buildClassifier(trainingSet);




        // 5. Evaluation
        DataSource test = new DataSource(args[1]);
        Instances testingSet = test.getDataSet();
        testingSet.setClassIndex(testingSet.numAttributes() - 1);

        Evaluation eval = new Evaluation(trainingSet);
        eval.evaluateModel(knn, testingSet);
        //System.out.println(model.toString());



        System.out.println("\nKNN Results ");
        System.out.println("======\nConfusion Matrix:");

        printMatrix(eval.confusionMatrix());

        return eval.errorRate();
    }

    /**
     * print confusion matrix
     * @param matrix double[][] array of data
     */
    private static void printMatrix(double[][] matrix) {
        for (int i = 0; i < matrix.length; ++i) {
            for (int j = 0; j < matrix[i].length; ++j) {
                System.out.format("%10s ", matrix[i][j]);
            }
            System.out.print("\n");
        }
    }


}
