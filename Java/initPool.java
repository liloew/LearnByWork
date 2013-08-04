import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;

public class initPool {
        public BlockingQueue<String> pool = new ArrayBlockingQueue<String>(100);
        
        public initPool() {
        	
        }
        
        public String randomStr(int num) {
            String result = "";
            for(int j=0; j<num; j++) {
                int intVal = (int)(Math.random()*26 + 97);
                result += (char) intVal;
            }

            return result;
        }

        public void enQueue(int num) {
            String result = randomStr(num);
            try {
            	System.out.println("Debug info: " + result);
                pool.put(result);
            } catch (InterruptedException e) {
                    e.printStackTrace();
                }
        }
        
        public void enQueue(String str) {
        	try {
				pool.put(str);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
        }

        public String deQueue() {
            String str = "";
            if (pool.isEmpty())
                System.exit(11);
            try {
                str = (String) pool.take();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

        return str;
    }
        
        public void initQueue(int k) {
        	for(int i=0; i<k; i++) {
        		enQueue(20);
        	}
        }
        
        public void initQueueQuery() {
        	new callProcedure(pool);
        }
}
