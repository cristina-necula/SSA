import client

def checkTestPassed(expected, actual):
    if expected == actual:
        return "PASSED"
    return "FAILED"

client = client.Client()
print 'Client started. '
print "Start running default tests"
print "\n"

print '1. createRole(root, root, role1) '
client.socket.send('createRole(root, root, role1)')
received = client.socket.recv(1024)
print 'received: ' + received
print 'Test 1 ' + checkTestPassed("ok", received)

print "\n"

print '2. createPermission(root,root,perm1,"r") '
client.socket.send('createPermission(root,root,perm1,"r")')
received = client.socket.recv(1024)
print 'received: ' + received
print 'Test 2 ' + checkTestPassed("ok", received)

print "\n"

print '3. assignRole(root,root,bob, role1) '
client.socket.send('assignRole(root, root, bob, role1)')
received = client.socket.recv(1024)
print 'received: ' + received
print 'Test 3 ' + checkTestPassed("ok", received)

print "\n"

print '4. creareResursa(alice, alice, /alice/cursuri.java, 1,"cursuri")'
client.socket.send('creareResursa(alice, alice, /alice/cursuri.java, 1,"cursuri")')
received = client.socket.recv(1024)
print 'received: ' + received
print 'Test 4 ' + checkTestPassed("ok", received)

print "\n"

print '5. assignPermission (alice,alice,/alice/cursuri.java,perm1)'
client.socket.send('assignPermission(alice,alice,/alice/cursuri.java,perm1)')
received = client.socket.recv(1024)
print 'received: ' + received
print 'Test 5 ' + checkTestPassed("ok", received)

print "\n"

print '6. addPermissionToRole(root,root,role1,perm1)'
client.socket.send('addPermissionToRole(root,root,role1,perm1)')
received = client.socket.recv(1024)
print 'received: ' + received
print 'Test 6 ' + checkTestPassed("ok", received)

print "\n"

print '7. readResursa(bob, bob, /alice/cursuri.java)'
client.socket.send('readResursa(bob, bob, /alice/cursuri.java)')
received = client.socket.recv(1024)
print 'received: ' + received
print 'Test 7 ' + checkTestPassed("ok, \"cursuri\"", received)

print "\n"

print '8. createRole(root,root,role2)'
client.socket.send('createRole(root,root,role2)')
received = client.socket.recv(1024)
print 'received: ' + received
print 'Test 8 ' + checkTestPassed("ok", received)

print "\n"

print '9. revokeRole(root,root,bob,role1)'
client.socket.send('revokeRole(root,root,bob,role1)')
received = client.socket.recv(1024)
print 'received: ' + received
print 'Test 9 ' + checkTestPassed("ok", received)

print "\n"

print '10. readResursa(bob, bob, /alice/cursuri.java)'
client.socket.send('readResursa(bob, bob, /alice/cursuri.java)')
received = client.socket.recv(1024)
print 'received: ' + received
print 'Test 10 ' + checkTestPassed("NotAuthorized", received)

print "\n"

print '11. assignRole(root,root,bob,role2)'
client.socket.send('assignRole(root,root,bob,role2)')
received = client.socket.recv(1024)
print 'received: ' + received
print 'Test 11 ' + checkTestPassed("ok", received)

print "\n"

print '12. readResursa(bob, bob, /alice/cursuri.java)'
client.socket.send('readResursa(bob, bob, /alice/cursuri.java)')
received = client.socket.recv(1024)
print 'received: ' + received
print 'Test 12 ' + checkTestPassed("NotAuthorized", received)

print "\n"

print '13. createHierarchy(root,root,role1,role2)'
client.socket.send('createHierarchy(root,root,role1,role2)')
received = client.socket.recv(1024)
print 'received: ' + received
print 'Test 13 ' + checkTestPassed("ok", received)

print "\n"

print '14. readResursa(bob, bob, /alice/cursuri.java)'
client.socket.send('readResursa(bob, bob, /alice/cursuri.java)')
received = client.socket.recv(1024)
print 'received: ' + received
print 'Test 14 ' + checkTestPassed("ok, \"cursuri\"", received)

print "\n"

print '15. createRole(root,root,role3)'
client.socket.send('createRole(root,root,role3)')
received = client.socket.recv(1024)
print 'received: ' + received
print 'Test 15 ' + checkTestPassed("ok", received)

print "\n"

print '16. createConstraint(root,root,role1,role3)'
client.socket.send('createConstraint(root,root,role1,role3)')
received = client.socket.recv(1024)
print 'received: ' + received
print 'Test 16 ' + checkTestPassed("ok", received)

print "\n"

print '17. assignRole(root,root,bob, role3)'
client.socket.send('assignRole(root,root,bob, role3)')
received = client.socket.recv(1024)
print 'received: ' + received
print 'Test 17 ' + checkTestPassed("Forbidden", received)

