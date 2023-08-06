Py Brain.

### Features

1.  Process Streams
    
     ``` .env
     Process 1   S1(t) ---> Pp1.1(t) ---> Pp1.2(t) ---> Pp1.3(t) ---> Pp1.4(t)  
     
     Process 2   S2(t) ---------------> Pp2.1(t) ----> Pp2.1(t)
                                \
                                 \
                                  \
                                  _\|
     Process 3                      T1 (t) -----> Tp1.1 (t) ----> Tp1.1 (t)
     ```
                                

2. Gather Any data from stream by index (t)

    ```python
    from pulathisi import Brain
    def stream_process_1(context:Brain.Context):
       (<index>,<data>)=context.get_current_value('source_name') # Get latest stored value 

    ```

3. Support for async process

4. Support for multiprocessing

5. In build Message queue

6. support for python development process                 