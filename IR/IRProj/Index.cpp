////////////////////////////////////////////
//                                        //
// Information Retrieval Assignment       //
//                                        //
// Robert Luk @ 2005                      //
// All rights reserved                    //
// Department of Computing                //
// The Hong Kong Polytechnic University   //
//                                        //
////////////////////////////////////////////
//                                        //
// This program should only be used for   //
// the information retrieval subjects     //
// (COMP425 and COMP433) of the           //
// Department of Computing, The Hong Kong //
// Polytechnic University.                //
//                                        //
////////////////////////////////////////////
//                                        //
// Acknowledgement:                       //
// The stemmer program (stem.cpp, stem.h) //
// is developed by Porter.                //
//                                        //
////////////////////////////////////////////

#include <stdio.h>
#include <stdlib.h>
#include "stem.h"

////////////////////////////////////////////
//                                        //
// Globle variable declaration            //
//                                        //
////////////////////////////////////////////

dic StopList;
stemmer StemProc;

////////////////////////////////////////////
//                                        //
// Function declaration                   //
//                                        //
////////////////////////////////////////////

// Delete the trailing newline and carriage return of a line
void FilterTrailNewline(char * line) {
	char c;

	c = line[strlen(line)-1];
	if ((c == '\n') || (c == '\r')) {
		line[strlen(line)-1] = '\0';
		c = line[strlen(line)-1];
		if ((c == '\n') || (c == '\r')) line[strlen(line)-1] = '\0';
	}

}

// Change the string into lower case
void LowerStr(char * s) {
	char * p;
	if (s == NULL) return;
	p = s;
	while (*p != '\0') {
		*p = (char) tolower(*p);
		p++;
	}
}

// Stopword list from the given file
void LoadStop(char *f) {

	FILE * fp = fopen(f, "rb");
	std::string x;
	StopList.clear();
	char line[1000];

		while (fgets(line, 1000, fp) != NULL) {
			FilterTrailNewline(line);
			LowerStr(line);
			x = line;
			StopList.insert(dic::value_type(x,1));
		}

	fclose(fp);
}

// Get the file name from the path p
void GetFileName(char * s, char * p) {

	char * t = p;
	if (s == NULL) return;
	if ((p == NULL) || (p[0] == '\0')) {
		s[0] = '\0';
		return;
	}

	t = p + strlen(p) - 1;

	while ((t >= p) && (t[0] != '\\')) {
		t--;
	}
	if (t[0] == '\\') t++;
	strcpy(s, t);
}

////////////////////////////////////////////
//                                        //
// Main Program                           //
//                                        //
////////////////////////////////////////////
int main() {

	FILE * fp;        // read data file name
	FILE * idxfp;     // read data file
	FILE * ofp;       // store postings
	FILE * ffp;       // store filename information
	char line[1000];  // store full path
	char file[1000];  // store file
	char id[1000];    // file id
	char str[1000];   // store token
	int count;        // logical word position
	long fcnt=0;      // file counter
	char c;
	int i;

	// hard code your directory that stores the data files
	// char * dir = "dir/b/s \\teach\\comp533\\data\\ > temp.txt\n";
	char * dir = "dir/b/s \\teach\\comp533\\proj\\trec\\data\\ > temp.txt\n";

	system(dir);

	fp = fopen("temp.txt","rb");
	ffp = fopen("file.txt","w");
	ofp = fopen("post.txt","w");
	LoadStop(".\\estop.lst");

	// Start processing each file in the temp.txt file
	while (fgets(line,1000, fp) != NULL) {
		// Get the file name
		FilterTrailNewline(line);
		strcpy(file,line);
		GetFileName(id,file);
		//if (fcnt > 200) goto here;
		// Process a data file
		idxfp = fopen(file,"rb");
		if (idxfp != NULL) {
			if ((fcnt % 100) == 0) printf("[%6ld]Reading file:%s\r\n",fcnt,file);
			count = 0;
			// Get a token
			while (fread(&c,1,1,idxfp) > 0) {
				if (isalpha(c) != 0) {
					str[0] = c;
					i=1;
					do {
						if ((fread(&c,1,1,idxfp) > 0) && (isalpha(c) != 0)) {
							str[i++] = c;
						}
						else break;
					} while (isalpha(c) != 0);
					str[i]='\0';
					LowerStr(str);
					if (StopList.find(str) == StopList.end()) {
						// token is not a stop word
						StemProc.Stem(str);
						fprintf(ofp,"%s %ld %d\n",str,fcnt,count++);
					}
				}
			}
			fclose(idxfp);
			fprintf(ffp,"%ld %ld @ %s %s\n",fcnt++,count,id,file);
		}
		else {
			fprintf(ffp,"%ld # s %s\r\n",fcnt++,file);
			printf("Could not find the file:: <%s>\r\n",file);
		}
	}

here:
	fclose(fp);
	fclose(ffp);
	fclose(ofp);
	StopList.clear();
	system("erase temp.txt");
	return 0;
}
