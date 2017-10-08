// Two phase matrix multiplication in Hadoop MapReduce
// Template file for homework #1 - INF 553 - Spring 2017
// - Wensheng Wu

import java.io.IOException;
import java.util.*;

// add your import statement here if needed
// you can only import packages from java.*;

import org.apache.hadoop.conf.Configuration;

import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.fs.FileSystem;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.LongWritable;

import org.apache.hadoop.mapreduce.lib.input.MultipleInputs;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.KeyValueTextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;


public class TwoPhase {

    // mapper for processing entries of matrix A
    public static class PhaseOneMapperA 
	extends Mapper<LongWritable, Text, Text, Text> {
	
	private Text outKey = new Text();
	private Text outVal = new Text();

	public void map(LongWritable key, Text value, Context context)
	    throws IOException, InterruptedException {
	    // fill in your code
		String[] matx = value.toString().split(",");
		outKey.set(matx[1]);
		outVal.set("A"+","+matx[0]+","+matx[2]);
		context.write(outKey,outVal);
	}

    }

    // mapper for processing entries of matrix B
    public static class PhaseOneMapperB
	extends Mapper<LongWritable, Text, Text, Text> {
	
	private Text outKey = new Text();
	private Text outVal = new Text();

	public void map(LongWritable key, Text value, Context context)
	    throws IOException, InterruptedException {
	    // fill in your code
		String[] matx = value.toString().split(",");
		outKey.set(matx[0]);
		outVal.set("B"+","+matx[1]+","+matx[2]);
		context.write(outKey,outVal);
	}
    }

    public static class PhaseOneReducer
	extends Reducer<Text, Text, Text, Text> {

	private Text outKey = new Text();
	private Text outVal = new Text();

	public void reduce(Text key, Iterable<Text> values, Context context) 
	    throws IOException, InterruptedException {	    
	    // fill in your code
		HashSet<String> hs1 = new HashSet<String>();
		HashSet<String> hs2 = new HashSet<String>();
		String tuple;
		String[] line,sline;
		int ai,bj,prd;
		String product;
		for (Text val:values){
			tuple = val.toString();
			line = tuple.split(",");
			if (line[0].equals("A")){
				hs1.add(tuple);
			}
			else if (line[0].equals("B")){
				hs2.add(tuple);
			}
		}
		for (String obj: hs1){
			line=obj.split(",");
			for (String sobj: hs2){
				sline = sobj.split(",");
				outKey.set(line[1]+","+sline[1]);
				ai=Integer.parseInt(line[2]);
				bj=Integer.parseInt(sline[2]);
				prd=ai*bj;
				product=Integer.toString(prd);
				outVal.set(product);
				context.write(outKey,outVal);
			}
		}																										
	}

    }

    public static class PhaseTwoMapper 
	extends Mapper<Text, Text, Text, Text> {
	
	private Text outKey = new Text();
	private Text outVal = new Text();

	public void map(Text key, Text value, Context context)
	    throws IOException, InterruptedException {
	    // fill in your code
		outKey.set(key);
		outVal.set(value);
		context.write(outKey,outVal);
	}
    }

    public static class PhaseTwoReducer 
	extends Reducer<Text, Text, Text, Text> {
	
	private Text outKey = new Text();
	private Text outVal = new Text();

	public void reduce(Text key, Iterable<Text> values, Context context)
	    throws IOException, InterruptedException {	 
	    // fill in your code
		int sum=0,num;
		String ssum;
		for (Text val:values){
			num=Integer.parseInt(val.toString());
			sum+=num;
		}
		ssum=Integer.toString(sum);
		outKey.set(key);
		outVal.set(ssum);
		context.write(outKey,outVal);
	}
    }


    public static void main(String[] args) throws Exception {
	Configuration conf = new Configuration();

	Job jobOne = Job.getInstance(conf, "phase one");

	jobOne.setJarByClass(TwoPhase.class);

	jobOne.setOutputKeyClass(Text.class);
	jobOne.setOutputValueClass(Text.class);

	jobOne.setReducerClass(PhaseOneReducer.class);

	MultipleInputs.addInputPath(jobOne,
				    new Path(args[0]),
				    TextInputFormat.class,
				    PhaseOneMapperA.class);

	MultipleInputs.addInputPath(jobOne,
				    new Path(args[1]),
				    TextInputFormat.class,
				    PhaseOneMapperB.class);

	Path tempDir = new Path("temp");

	FileOutputFormat.setOutputPath(jobOne, tempDir);
	jobOne.waitForCompletion(true);


	// job two
	Job jobTwo = Job.getInstance(conf, "phase two");
	

	jobTwo.setJarByClass(TwoPhase.class);

	jobTwo.setOutputKeyClass(Text.class);
	jobTwo.setOutputValueClass(Text.class);

	jobTwo.setMapperClass(PhaseTwoMapper.class);
	jobTwo.setReducerClass(PhaseTwoReducer.class);

	jobTwo.setInputFormatClass(KeyValueTextInputFormat.class);

	FileInputFormat.setInputPaths(jobTwo, tempDir);
	FileOutputFormat.setOutputPath(jobTwo, new Path(args[2]));
	
	jobTwo.waitForCompletion(true);
	
	FileSystem.get(conf).delete(tempDir, true);
	
    }
}