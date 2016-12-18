import client

client = client.Client()
print 'Client started. '

print "Start running default tests"

print '1. createRole(root, root, role1)'
client.socket.send('createRole(root, root, role1)')
print 'received: ' + client.socket.recv(1024)

print '2. createPermission(bob,bob,perm1,r)'
client.socket.send('createPermission(bob,bob,perm1,r)')
print 'received: ' + client.socket.recv(1024)

print '3. createPermission(root,root,perm1,r)'
client.socket.send('createPermission(root,root,perm1,r)')
print 'received: ' + client.socket.recv(1024)

print '4. assignRole(root,root,bob, role1)'
client.socket.send('assignRole(root,root,bob,role1)')
print 'received: ' + client.socket.recv(1024)

print '5. creareResursa(alice, alice, /alice/cursuri.java, 1,cursuri)'
client.socket.send('creareResursa(alice, alice, /alice/cursuri.java, 1,cursuri)')
print 'received: ' + client.socket.recv(1024)

print '6. assignPermission(bob, bob, /alice/cursuri.java,perm1)'
client.socket.send('assignPermission(bob, bob, /alice/cursuri.java,perm1)')
print 'received: ' + client.socket.recv(1024)

print '7. assignPermission (alice,alice,/alice/cursuri.java,perm1)'
client.socket.send('assignPermission(alice,alice,/alice/cursuri.java,perm1)')
print 'received: ' + client.socket.recv(1024)

print '8. readResursa(bob, bob, /alice/cursuri.java)'
client.socket.send('readResursa(bob, bob, /alice/cursuri.java)')
print 'received: ' + client.socket.recv(1024)

print '9. addPermissionToRole(root,root,role1,perm1)'
client.socket.send('addPermissionToRole(root,root,role1,perm1)')
print 'received: ' + client.socket.recv(1024)

print '10. readResursa(bob, bob, /alice/cursuri.java)'
client.socket.send('readResursa(bob, bob, /alice/cursuri.java)')
print 'received: ' + client.socket.recv(1024)

print '11. createRole(root, root, role2)'
client.socket.send('createRole(root, root, role2)')
print 'received: ' + client.socket.recv(1024)

print '12. revokeRole(root,root,bob,role2)'
client.socket.send('revokeRole(root,root,bob,role2)')
print 'received: ' + client.socket.recv(1024)

print '13. assignRole(root,root,bob,role2)'
client.socket.send('assignRole(root,root,bob,role2)')
print 'received: ' + client.socket.recv(1024)

print '14. revokeRole(root,root,bob,role2)'
client.socket.send('revokeRole(root,root,bob,role2)')
print 'received: ' + client.socket.recv(1024)

print '15. createConstraint(root,root,role1,role2)'
client.socket.send('createConstraint(root,root,role1,role2)')
print 'received: ' + client.socket.recv(1024)

print '16. assignRole(root,root,bob, role2)'
client.socket.send('assignRole(root,root,bob, role2)')
print 'received: ' + client.socket.recv(1024)