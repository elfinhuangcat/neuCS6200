package classifier;

import java.util.Arrays;
import java.util.Random;

import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.classifiers.bayes.NaiveBayes;
import weka.classifiers.functions.Logistic;
import weka.classifiers.functions.SMO;
import weka.classifiers.lazy.IBk;
import weka.classifiers.trees.J48;
import weka.classifiers.trees.NBTree;
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;
import data_preprocess.MyResampler;
/**
 * This class provides the method to run different classifiers 
 * according to user-entered argument. It runs without any 
 * data preprocessing, cost matrix, bagging or boosting.
 * @author yaxin
 *
 */
public class DiffClassifier {
	private int fold; // Cross validation fold num
	private int seed; // Random seed for reordering the training data
	private Classifier model;

	public DiffClassifier() {
		this.fold = 10;
		this.seed = (int) System.currentTimeMillis();
		this.model = null;
	}
	public DiffClassifier(int fold, int seed) {
		this.fold = fold;
		this.seed = seed;
		this.model = null;
	}

	public static void main(String[] args) {
		String[] arguments = {"/home/yaxin/workspace/DataMining_Project/data/train.arff",
		"-knn", "-K", "3"};
		try {
			DiffClassifier.run(arguments);
		} catch (Exception e) {
			e.printStackTrace();
			System.exit(1);
		}
	}

	/***************************************************
	 * @param args[0] train arff path
	 * @param args[1] choice of classifier: ["-c45", "-knn", "-logr", "-nb", "-nbt", "-smo"]
	 * @param args[after 1] options passed to the classifier.
	 * @see For available options please check the correspongding weka doc.
	 */
	public static void run(String[] args) throws Exception {
		// Read training data
		DataSource trainSource = new DataSource(args[0]);
		Instances trainData = trainSource.getDataSet();
		trainData.setClassIndex(trainData.numAttributes() - 1);

		// Resample:
		Instances balancedTrainData = MyResampler.resampleToBalance(trainData);

		// Build and evaluate the classifier using cross validation:
		// TODO right now we use the default folds and seed
		DiffClassifier classifyTask = new DiffClassifier();
		classifyTask.buildAndEvaluate(balancedTrainData, 
				Arrays.copyOfRange(args, 1, args.length));

	}

	/**
	 * 
	 * @param trainData the training instances
	 * @param args[0] choice of classifier: ["-c45", "-knn", "-logr", "-nb", "-nbt", "-smo"]
	 * @param args[after 0] options passed to the classifier.
	 */
	public void buildAndEvaluate(Instances trainData, String[] args) {
		this.setModel(args[0], Arrays.copyOfRange(args, 1, args.length));
		System.out.println("Options: " + Arrays.toString(this.model.getOptions()));

		// Randomize data
		Random rand = new Random(this.seed);
		trainData.randomize(rand);

		// TODO what's this?
		// In case your data has a nominal class and you wanna perform stratified cross-validation:
		// randData.stratify(folds);

		double sumErrorRate = 0;
		for (int n = 0; n < this.fold; ++n) {
			Instances trainFold = trainData.trainCV(this.fold, n);
			Instances testFold = trainData.testCV(this.fold, n);
			try {
				this.model.buildClassifier(trainFold);

				// Evaluate:
				Evaluation eval = new Evaluation(trainFold);
				eval.evaluateModel(this.model, testFold);
				System.out.println("INFO - Statistics for " + (n+1) + "th fold: \n"
						+ "Error rate: " + eval.errorRate() + "\nConfusion Matrix: ");
				for (int i = 0; i < eval.confusionMatrix().length; ++i) {
					for (int j = 0; j < eval.confusionMatrix()[i].length; ++j) {
						System.out.print(eval.confusionMatrix()[i][j] + "\t");
					}
					System.out.println();
				}
				sumErrorRate += eval.errorRate();
			} catch (Exception e) {
				System.out.println("ERROR - cannot load the train/test fold.");
				e.printStackTrace();
			}
		}
		System.out.println("************* Average Error Rate: " + 
				sumErrorRate / this.fold + " *************");
	}


	public int getFold() {
		return fold;
	}
	public void setFold(int fold) {
		this.fold = fold;
	}
	public int getSeed() {
		return seed;
	}
	public void setSeed(int seed) {
		this.seed = seed;
	}
	public Classifier getModel() {
		return model;
	}

	/**
	 * @param modelChoice one of: ["-c45", "-knn", "-logr", "-nb", "-nbt", "-smo"]
	 * @param options the options of this model
	 */
	public void setModel(String modelChoice, String[] options) {
		if (modelChoice.equals("-c45")) {
			this.model = new J48();
			System.out.println("====================\nClassifier Name: C45 Decision Tree");		
		}
		else if (modelChoice.equals("-knn")) {
			this.model = new IBk();
			System.out.println("====================\nClassifier Name: KNN");
		}
		else if (modelChoice.equals("-logr")) {
			this.model = new Logistic();
			System.out.println("====================\nClassifier Name: Logistic Regression");
		}
		else if (modelChoice.equals("-nb")) {
			this.model = new NaiveBayes();
			System.out.println("====================\nClassifier Name: Naive Bayes");
		}
		else if (modelChoice.equals("-nbt")) {
			this.model = new NBTree();
			System.out.println("====================\nClassifier Name: Naive Bayes Decision Tree");
		}
		else if (modelChoice.equals("-smo")) {
			this.model = new SMO();
			System.out.println("====================\nClassifier Name: SMO");
		}
		else {
			System.out.println("ERROR - wrong choice of classifier.");
			System.exit(1);
		}
		try {
			this.model.setOptions(options);
		} catch (Exception e) {
			System.out.println("ERROR - model options failed to be set.");
			e.printStackTrace();
			System.exit(1);
		}
	}

}