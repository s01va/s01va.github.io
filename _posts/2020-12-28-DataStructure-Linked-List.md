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

사고과정 따라가기/익숙해지기

1. 구현

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

   

   ![00](https://s01va.github.io/assets/images/2020-12-28-DataStructure-Linked-List/0.jpg)

   

2. 사용

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

   

3. 과정

   ```python
   node_mgmt = NodeMgmt(0)
   ```

   `class NodeMgmt`의 초기화 과정 `__init__`을 거쳐감으로써 생성되는 Node 객체

   ![01](https://s01va.github.io/assets/images/2020-12-28-DataStructure-Linked-List/1.jpg)

   ```python
   for data in range(1,10):
   	node_mgmt.add(data)
   ```

   반복문 중 `node_mgmt.add(1)` 과정

   ![02](https://s01va.github.io/assets/images/2020-12-28-DataStructure-Linked-List/2.jpg)

   

   반복문 중 `node_mgmt.add(2)` 과정

   ![03](https://s01va.github.io/assets/images/2020-12-28-DataStructure-Linked-List/3.jpg)

   

   ```python
   node_mgmt.desc()
   ```

   ![04](https://s01va.github.io/assets/images/2020-12-28-DataStructure-Linked-List/4.jpg)

   ![05](https://s01va.github.io/assets/images/2020-12-28-DataStructure-Linked-List/5.jpg)

