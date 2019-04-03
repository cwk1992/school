///////////////////////////////////////////////////////////////////////////////////////
//
// Author: Robert Luk
// Year: 2010
// Robert Luk (c) 2010 
//
// Interactive Retrieval using the Integrated Inverted Index Class:
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

	// Initialize the Hash Table
	InvFile.MakeHashTable(13023973);

	printf("Loading Inverted File\r\n");
	InvFile.Load("InvFile.txt");

	printf("Load Document Lengths\r\n");
	InvFile.LoadDocRec("InvFile.doc");

	// Start interactive retrieval
	InvFile.Retrieval();

	return 0;
}
