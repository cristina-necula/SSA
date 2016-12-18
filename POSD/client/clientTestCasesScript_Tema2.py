import client

client = client.Client()
print 'Client started. '

print '0. creareResursa(alice, alice, /alice/cursuri, 0)'
client.socket.send('creareResursa(alice, alice, /alice/cursuri, 0)')
print 'received: ' + client.socket.recv(1024)

print "Start running default tests"

print '1. createRole(bob, bob, role1)'
client.socket.send('createRole(bob, bob, role1)')
print 'received: ' + client.socket.recv(1024)

print '2. createRole(root, root, role1)'
client.socket.send('createRole(root, root, role1)')
print 'received: ' + client.socket.recv(1024)

print '3. changeRights(role1, "r")'
client.socket.send('changeRights(role1, "r")')
print 'received: ' + client.socket.recv(1024)

print '4. assignRole(bob, role1)'
client.socket.send('assignRole(bob, role1)')
print 'received: ' + client.socket.recv(1024)

print '5. creareResursa(alice, alice, /alice/cursuri/cursuri.java, 1,"cursuri")'
client.socket.send('creareResursa(alice, alice, /alice/cursuri/cursuri.java, 1,"cursuri")')
print 'received: ' + client.socket.recv(1024)

print '6. readResursa(bob, bob, /alice/cursuri)'
client.socket.send('readResursa(bob, bob, /alice/cursuri)')
print 'received: ' + client.socket.recv(1024)

print '7. addRights(bob,bob,/alice/cursuri,role1)'
client.socket.send('addRights(bob,bob,/alice/cursuri,role1)')
print 'received: ' + client.socket.recv(1024)

print '8. addRights(alice,alice,/alice/cursuri,role1)'
client.socket.send('addRights(alice,alice,/alice/cursuri,role1)')
print 'received: ' + client.socket.recv(1024)

print '9. readResursa(bob, bob, /alice/cursuri/cursuri.java)'
client.socket.send('readResursa(bob, bob, /alice/cursuri/cursuri.java)')
print 'received: ' + client.socket.recv(1024)

print '10. writeResource(alice, alice, /alice/cursuri/cursuri.java, "cursuri2")'
client.socket.send('writeResource(alice, alice, /alice/cursuri/cursuri.java, "cursuri2")')
print 'received: ' + client.socket.recv(1024)

print '11. writeResource(bob, bob, /alice/cursuri/cursuri.java, "cursuri3")'
client.socket.send('writeResource(bob, bob, /alice/cursuri/cursuri.java, "cursuri3")')
print 'received: ' + client.socket.recv(1024)

print '12. changeRights(role1, "w")'
client.socket.send('changeRights(role1, "w")')
print 'received: ' + client.socket.recv(1024)

print '13. writeResource(bob, bob, /alice/cursuri/cursuri.java, "cursuri3")'
client.socket.send('writeResource(bob, bob, /alice/cursuri/cursuri.java, "cursuri3")')
print 'received: ' + client.socket.recv(1024)

print '14. readResursa(bob, bob, /alice/cursuri/cursuri.java)'
client.socket.send('readResursa(bob, bob, /alice/cursuri/cursuri.java)')
print 'received: ' + client.socket.recv(1024)

print '15. createRole(root, root, role2)'
client.socket.send('createRole(root, root, role2)')
print 'received: ' + client.socket.recv(1024)

print '16. changeRights(role2, "r")'
client.socket.send('changeRights(role2, "r")')
print 'received: ' + client.socket.recv(1024)

print '17. assignRole(bob, role2)'
client.socket.send('assignRole(bob, role2)')
print 'received: ' + client.socket.recv(1024)

print '18. addRights(alice,alice,/alice/cursuri,role2)'
client.socket.send('addRights(alice,alice,/alice/cursuri,role2)')
print 'received: ' + client.socket.recv(1024)

print '19. readResursa(bob, bob, /alice/cursuri/cursuri.java)'
client.socket.send('readResursa(bob, bob, /alice/cursuri/cursuri.java)')
print 'received: ' + client.socket.recv(1024)