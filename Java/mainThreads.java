import java.util.ArrayList;
import java.util.List;

public class mainThreads {
    public static void main (String[] args) {
    	initPool inPool = new initPool();
    	List<Thread> list = new ArrayList<Thread>();
    	//inPool.initQueue(100);
    	inPool.initQueueQuery();
    	
        for (int i=0; i<10; i++) {
        	Thread th = new Thread(new callProcedure(inPool));
        	th.start();
        	list.add(th);
        }
        
        System.out.println("Waiting for Threads");
    }
}
