///////////////////////////////////////////////////////////////////////////////////////
//
// Author: Robert Luk
// Year: 2010
// Robert Luk (c) 2010 
//
// Compute Document Lengths: (make sure the InvFile.txt is available)
// This software is made available only to students studying COMP433 (Information
// Retreieval). It should not be used or distributed without consent by the author.
//
////////////////////////////////////////////////////////////////////////////////////////
#include<stdio.h>
#include<stdlib.h>
#include<string.h>

#include "IInvFile.h"

// Integrated Inverted Index (see lecture notes on Implementation)
IInvFile InvFile;

int main() {
	char tmp[10000];
	char str[1000];
	int docid;
	int loc;
	int cnt=0;

	// Initialize the Hash Table
	InvFile.MakeHashTable(13023973);

	printf("Loading Inverted File\r\n");
	InvFile.Load("InvFile.txt");
	printf("Creating Document Records (size = %d)\r\n", InvFile.MaxDocid+1);
	InvFile.MakeDocRec();	// allocate document records
	printf("Compute Document Lengths...\r\n");
	InvFile.DocLen(InvFile.Files);
	printf("Save Document Lengths\r\n");
	InvFile.SaveDocRec("InvFile.doc");

	return 0;
}
