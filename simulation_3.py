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
simulation_time = 2 #give the network sufficient time to transfer all packets before quitting

if __name__ == '__main__':
    object_L = [] #keeps track of objects, so we can kill their threads
    Router_A_Table = []
    Router_B_Table = []
    Router_C_Table = []
    Router_D_Table = []

    #create part3 network topology
    Host_1 = network.Host(1) #mobile device
    object_L.append(Host_1)
    Host_2 = network.Host(2) #laptop
    object_L.append(Host_2)
    Host_3 = network.Host(3) #Server 3
    object_L.append(Host_3)
    Host_4 = network.Host(4)  #Server 4
    object_L.append(Host_4)

    #Router tables format (in_interface, dst_addr, out_interface)
    Host_1_to_A_3 = (0, 3, 0)  # from mobile device to server 3
    Host_1_to_A_4 = (0, 4, 0)  # from mobile device to server 4
    Host_2_to_A_3 = (1, 3, 1)  # from laptop to server 3
    Host_2_to_A_4 = (1, 4, 1)  # from laptop to server 4
    Router_A_Table.append(Host_1_to_A_3)
    Router_A_Table.append(Host_1_to_A_4)
    Router_A_Table.append(Host_2_to_A_3)
    Router_A_Table.append(Host_2_to_A_4)
    Router_A = network.Router(name='A', intf_count=2, max_queue_size=router_queue_size, router_table=Router_A_Table)
    object_L.append(Router_A)

    Router_A_to_B_3 = (0, 3, 0) # mobile device -> A -> B
    Router_A_to_B_4 = (0, 4, 0) # mobile device -> A -> B
    Router_B_Table.append(Router_A_to_B_3)
    Router_B_Table.append(Router_A_to_B_4)
    Router_B = network.Router(name='B', intf_count=1, max_queue_size=router_queue_size, router_table=Router_B_Table)
    object_L.append(Router_B)

    Router_A_to_C_3 = (0, 3, 0) # laptop -> A -> C
    Router_A_to_C_4 = (0, 4, 0) # laptop -> A -> C
    Router_C_Table.append(Router_A_to_C_3)
    Router_C_Table.append(Router_A_to_C_4)
    Router_C= network.Router(name='C', intf_count=1, max_queue_size=router_queue_size, router_table=Router_C_Table)
    object_L.append(Router_C)

    Router_B_to_D_3 = (0, 3, 0) # mobile device -> A -> B -> D -> 3
    Router_B_to_D_4 = (0, 4, 1) # mobile device -> A -> B -> D -> 4
    Router_C_to_D_3 = (1, 3, 0) # laptop -> A -> B -> D -> 3
    Router_C_to_D_4 = (1, 4, 1) # laptop -> A -> B -> D -> 4
    Router_D_Table.append(Router_B_to_D_3)
    Router_D_Table.append(Router_B_to_D_4)
    Router_D_Table.append(Router_C_to_D_3)
    Router_D_Table.append(Router_C_to_D_4)
    Router_D= network.Router(name='D', intf_count=2, max_queue_size=router_queue_size, router_table=Router_D_Table)
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

    Host_1.udt_send(3,' Hello')
    #Host_2.udt_send(4,' Sup dog')

    '''
    #create some send events    
    #udt_send(self, dst_addr, src_addr, data_S):
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