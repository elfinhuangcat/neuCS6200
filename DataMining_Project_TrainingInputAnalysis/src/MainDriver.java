import java.io.*;
public class MainDriver {
	private final static int FIELDNUM = 15;
	public static void main(String[] args) throws IOException {
		// args[0]: path to train.data
		BufferedReader br = new BufferedReader(new FileReader(args[0]));
		BufferedWriter bw = new BufferedWriter(new FileWriter("log.txt", false));
		
		int[] missingCount = new int[FIELDNUM];
		for (int i = 0; i < FIELDNUM; ++i) {
			missingCount[i] = 0;
		}
		
		String line = null;
		while ((line=br.readLine())!=null) {
			// Look for the "?" in this line
			if (line.contains("?")) {
				// split
				String[] content = line.split(", ");
				for (int j = 0; j < FIELDNUM; ++j) {
					if (content[j].equals("?")) {
						missingCount[j] += 1;
					}
				}
				bw.write(line + "\n");
			}
		}
		br.close();
		bw.close();
		System.out.println("Missing Value Count:");
		for (int k = 0; k < FIELDNUM; ++k) {
			System.out.println("Col " + k + " : " + missingCount[k]);
		}
	}
}