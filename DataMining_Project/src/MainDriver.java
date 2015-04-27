import java.io.File;
import java.io.IOException;

import myutil.Log;

import classifier.DiffClassifier;

public class MainDriver {
	/**
	 * 
	 * @param args
	 * @throws IOException 
	 * @throws Exception 
	 */
	public static void main(String[] args) throws IOException {
		String trainArffPath = "/home/elfin/workspace/OngoingProjects/DataMining_Project/data/train.arff";
		String logFilePath = "/home/elfin/workspace/OngoingProjects/DataMining_Project/data/log";
		File logFile = new File(logFilePath);
		if (logFile.exists()) {
			logFile.delete();
		}
		logFile.createNewFile();
		
		MainDriver.runAllClassifiers(logFilePath, trainArffPath);
	}
	
	/**
	 * This is the method to run cross validation on all classifiers to see 
	 * which has the better average performance (lower error rate).
	 * @param logFilePath the path to the log file
	 * @param trainArffPath the path to the training set arff file.
	 */
	public static void runAllClassifiers(String logFilePath, String trainArffPath) {
		double errorRate = 0;
		try {
			// 1. C4.5 decision tree
			// 1.1 Laplace smoothing is applied. Vary the pruning confidence:
			Log.addLogToThisPath("### C4.5 smoothing applied, vary pruning confidence:\n", logFilePath);
			double[] pruningConf = {0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50};
			for (Double threshold : pruningConf) {
				errorRate = DiffClassifier.run(new String[] {logFilePath, trainArffPath, 
						"-c45", "-C", threshold.toString(), "-A"});
				Log.addLogToThisPath("*************[-c45 -C " + threshold.toString() + 
						" -A] " + errorRate + " *************", logFilePath);
			}
			// 1.2 Laplace smoothing is applied. Use reduced error pruning.
			Log.addLogToThisPath("### C4.5 smoothing applied, use reduced error pruning:\n", logFilePath);
			errorRate = DiffClassifier.run(new String[] {logFilePath, trainArffPath, 
					"-c45", "-R", "-A"}); 
			Log.addLogToThisPath("*************[-c45 -R -A] " + errorRate + " *************", logFilePath);
			
			// 1.3 Turn off subtree raising. Laplace smoothing is applied. Vary the pruning confidence:
			Log.addLogToThisPath("### C4.5 smoothing applied, TURN OFF SUBTREE RAISING, " +
					"vary pruning confidence:\n", logFilePath);
			for (Double threshold : pruningConf) {
				errorRate = DiffClassifier.run(new String[] {logFilePath, trainArffPath, 
						"-c45", "-C", threshold.toString(), "-S", "-A"});
				Log.addLogToThisPath("*************[-c45 -C " + threshold.toString() + 
						" -S -A] " + errorRate + " *************", logFilePath);
			}
			
			// 1.4 Turn off subtree raising. Laplace smoothing is applied. Use reduced error pruning.
			Log.addLogToThisPath("### C4.5 smoothing applied, TURN OFF SUBTREE RAISING," +
					" use reduced error pruning:\n", logFilePath);
			errorRate = DiffClassifier.run(new String[] {logFilePath, trainArffPath, 
					"-c45", "-R", "-S", "-A"}); 
			Log.addLogToThisPath("*************[-c45 -R -S -A] " + errorRate + " *************", logFilePath);
			
			// TODO above already tested
			// 2. KNN: with varied K value
			
			
		} catch (Exception e) {
			e.printStackTrace();
			System.exit(1);
		}
	}
	
	/*
	public static void main(String[] args) throws Exception {
		if (args[0].equals("-transtrain")) {
			if (args.length != 3) {
				//TODO: print usage error
				System.exit(1);
			}
			TransTrainArff.main(Arrays.copyOfRange(args, 1, 3));
		}
		else if (args[0].equals("-transtest")) {
			if (args.length != 3) {
				//TODO: print usage error
				System.exit(1);
			}
			TransTestArff.main(Arrays.copyOfRange(args, 1, 3));
		}
		else if (args[0].equals("-diffcls")) {
			DiffClassifier.run(Arrays.copyOfRange(args, 1, args.length));
		}
		else {
			// TODO: print usage error
			System.exit(1);
		}
	}
	*/
}