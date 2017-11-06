'''
Created on Oct 12, 2016

@author: mwitt_000
'''
import network_3 as network
import link_3 as link
import threading
from time import sleep

##configuration parameters
router_queue_size = 0 #0 means unlimited
simulation_time = 1 #give the network sufficient time to transfer all packets before quitting

if __name__ == '__main__':
    object_L = [] #keeps track of objects, so we can kill their threads

    #create part3 network topology
    Host_1 = network.Host(1) #mobile device
    object_L.append(Host_1)
    Host_2 = network.Host(2) #laptop
    object_L.append(Host_2)
    Host_3 = network.Host(3) #Server 3
    object_L.append(Host_3)
    Host_4 = network.Host(4)  #Server 4
    object_L.append(Host_4)
    Router_A = network.Router(name='A', intf_count=2, max_queue_size=router_queue_size)
    object_L.append(Router_A)
    Router_B = network.Router(name='B', intf_count=1, max_queue_size=router_queue_size)
    object_L.append(Router_B)
    Router_C= network.Router(name='C', intf_count=1, max_queue_size=router_queue_size)
    object_L.append(Router_C)
    Router_D= network.Router(name='D', intf_count=2, max_queue_size=router_queue_size)
    object_L.append(Router_D)


    #create a Link Layer to keep track of links between network nodes
    link_layer = link.LinkLayer()
    object_L.append(link_layer)

    #add links for part3 network topology
    link_layer.add_link(link.Link(Host_1, 0, Router_A, 0, 50))
    link_layer.add_link(link.Link(Host_2, 0, Router_A, 1, 50))
    link_layer.add_link(link.Link(Router_A, 0, Router_B, 0, 50))
    link_layer.add_link(link.Link(Router_A, 1, Router_C, 0, 50))
    link_layer.add_link(link.Link(Router_B, 0, Router_D, 0, 50))
    link_layer.add_link(link.Link(Router_C, 0, Router_D, 1, 50))
    link_layer.add_link(link.Link(Router_D, 0, Host_3, 0, 50))
    link_layer.add_link(link.Link(Router_D, 1, Host_4, 0, 50))

    #start all part3 topology threads
    thread_L = []
    thread_L.append(threading.Thread(name=Host_1.__str__(), target=Host_1.run))
    thread_L.append(threading.Thread(name=Host_2.__str__(), target=Host_2.run))
    thread_L.append(threading.Thread(name=Host_3.__str__(), target=Host_3.run))
    thread_L.append(threading.Thread(name=Host_4.__str__(), target=Host_4.run))
    thread_L.append(threading.Thread(name=Router_A.__str__(), target=Router_A.run))
    thread_L.append(threading.Thread(name=Router_B.__str__(), target=Router_B.run))
    thread_L.append(threading.Thread(name=Router_C.__str__(), target=Router_C.run))
    thread_L.append(threading.Thread(name=Router_D.__str__(), target=Router_D.run))
    
    thread_L.append(threading.Thread(name="Network", target=link_layer.run))
    
    for t in thread_L:
        t.start()


    '''
    #create some send events    
    for i in range(3):
        client.udt_send(2, 'Sample data %d' % i)
    '''
    
    
    #give the network sufficient time to transfer all packets before quitting
    sleep(simulation_time)
    
    #join all threads
    for o in object_L:
        o.stop = True
    for t in thread_L:
        t.join()
        
    print("All simulation threads joined")



# writes to host periodically