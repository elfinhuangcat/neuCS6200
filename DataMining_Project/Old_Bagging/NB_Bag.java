package classifier;

import weka.classifiers.Evaluation;
import weka.classifiers.bayes.NaiveBayes;
import weka.classifiers.meta.Bagging;
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;

public class NB_Bag {

	public static double run(String args[]) throws Exception{
		DataSource source = new DataSource(args[0]);
		Instances data = source.getDataSet();
		data.setClassIndex(data.numAttributes() - 1);
			// Use Bagging	
			Bagging bagging = new Bagging();
			NaiveBayes nbModel = new NaiveBayes();
			bagging.setClassifier(nbModel);
			bagging.buildClassifier(data);
			
			// Evaluation:
			Evaluation eval = new Evaluation(data);
			Instances testData = new DataSource(args[1]).getDataSet();
			testData.setClassIndex(testData.numAttributes() - 1);
			eval.evaluateModel(bagging, testData);
			System.out.println(eval.toSummaryString("\nNBTree Results with "
					+ "Bagging\n==============\n", false));
			System.out.println("======\nConfusion Matrix:");
			double[][] confusionM = eval.confusionMatrix();
			for (int i = 0; i < confusionM.length; ++i) {
				for (int j = 0; j < confusionM[i].length; ++j) {
					System.out.format("%10s ", confusionM[i][j]);
				}
				System.out.print("\n");
			}
			return eval.errorRate();
	}
}