import java.io.IOException;
import java.util.Arrays;

import trans_to_arff.TransTestArff;
import trans_to_arff.TransTrainArff;
import classifier.DiffClassifier;
import classifier.NBT_Ada;
import classifier.NBT_Ada_Diff_Iter_Num;
import classifier.NBT_Ada_Multi_Tries;

public class MainDriver {
	/**
	 * 
	 * @param args
	 * @throws Exception 
	 */
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
}