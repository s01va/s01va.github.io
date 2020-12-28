---
layout: single
title: "자료구조: Linked list"
description: "자료구조 기초"
date: 2020-12-28 12:37:00 -0400
# modified: 
tags:
- DataStructure
- BasicCS
comments: true
share: true
---

## Linked List

```python
# -*- coding: utf-8 -*-

class Node:
	def __init__(self, data, next=None):
		self.data = data
		self.next = next

class NodeMgmt:
	def __init__(self, data):
		self.head = Node(data)

	def add(self, data):
		if self.head == '':
			self.head = Node(data)
		else :
			node = self.head
			while node.next:
				node = node.next
			node.next = Node(data)

	def desc(self):
		node = self.head
		while node:
			print(node.data)
			node = node.next

	def delete(self, data):
		if self.head == '':
			print("해당 값을 가진 노드 없음.")
			return

		if self.head.data == data:	# self.head를 삭제해야 할 경우
			temp = self.head
			self.head = self.head.next
			del temp
		else:	# self.head가 아닌 노드를 삭제할 경우
			node = self.head
			while node.next:
				if node.next.data == data:
					temp = node.next
					node.next = node.next.next
					del temp
					return
				else:
					node = node.next

	def search_node(self, data):
		node = self.head
		while node:
			if node.data == data:
				return node
			else:
				node = node.next
```

```python
node_mgmt = NodeMgmt(0)

for data in range(1,10):
	node_mgmt.add(data)

print("- desc() start:")
node_mgmt.desc()
print("- desc() end")

print("- print head address: " + str(node_mgmt.head))

print("- delete head node")
node_mgmt.delete(0)

print("- desc() start:")
node_mgmt.desc()
print("- desc() end")

print("- delete node 4")
node_mgmt.delete(4)

print("- desc() start:")
node_mgmt.desc()
print("- desc() end")
```