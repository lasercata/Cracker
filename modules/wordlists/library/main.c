/*
author : Elerias
date : 10/06/2020
version : 1.0
*/

#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>

#define I_SIZE_TABLE 1
#define I_SIZE_FILE 2
#define I_N_CHAR 3
#define I_N_DIFF_CHAR 4
#define I_MIN_CODE_POINT 5
#define I_MAX_CODE_POINT 6
#define I_N_WORDS 7
#define I_L_SMALLER_WORD 8
#define I_L_BIGGER_WORD 9
#define I_AVERAGE_L_WORD 10
#define I_MEDIAN_L_WORD 11
#define I_L_TABLE 12
#define I_O_TABLE 268

unsigned long int getc_utf8(FILE* f);
unsigned long long int* analyzeWordlist(const char* filename, const char* separators, const int encoding);

unsigned long int getc_utf8(FILE* f) // Return the next point of code in utf-8.
{
    unsigned long int c = (unsigned long int) getc(f);
    if (c == EOF) return EOF;
    if (c < 128)
    {
        return c;
    }
    if (c < 224)
    {
        return ((c - 192) << 6) | ((unsigned long int) getc(f) - 128);
    }
    if (c < 240)
    {
        return ((c - 224) << 12) | (((unsigned long int) getc(f) - 128) << 6) | ((unsigned long int) getc(f) - 128);
    }
    return ((c - 240) << 18) | (((unsigned long int) getc(f) - 128) << 12) | (((unsigned long int) getc(f) - 128) << 6) | ((unsigned long int) fgetc(f) - 128);
}

unsigned long long int* analyzeWordlist(const char* filename, const char* separators, const int encoding)
/* Return an array.
The separators delimit the line. They are encoded in one octet. N.B. : The 0D ASCII char is ignored before OA.
The index 0 is the function had a good process else 1 if file not found, 2 if denied access, 3 if allocation 1 error, 4 if allocation 2 error.
The index 1 corresponds to the length of the table.
The index 2 corresponds to the size of the file in octets.
The index 3 corresponds to the number of characters in the file (with separators).
The index 4 corresponds to the number of different characters in the wordlist (without the separators).
The index 5 corresponds to the character whose code point is the minimum.
The index 6 corresponds to the character whose code point is the maximum.
The index 7 corresponds to the number of words in the wordlist.
The index 8 corresponds to the length of the smaller word in the wordlist.
The index 9 corresponds to the length of the bigger word in the wordlist.
The index 10 corresponds to the average length * 1000 of a word in the wordlist.
The index 11 corresponds to the median length * 10 of a word in the wordlist.
The index m between 12 and 266 correspond to the number of words of length m - 10 (0-254).
The index 267 corresponds to the number of words of length >= 255.
The index n correspond to the number of occurrences of the char n - 268.
Encoding :  0 for one-octet encoding (ASCII, latin-x ...)
            1 for UTF-8
*/
{
    FILE* f = fopen(filename, "r"); // Open the file
    if (f == NULL) // If the file can't be opened
    {
        static unsigned long long int table[1];
        printf("Error in wordlist_analyzer.dll :\n");
        printf("Cannot open ");
        for (int i = 0 ; i < strlen(filename) ; i++)
        {
            printf("%c", filename[i]);
        }
        if (errno == EINVAL)
        {
            printf("\nFile not found.\n");
            table[0] = 1;
        }
        else if (errno == EACCES)
        {
            printf("\nAccess to file denied.\n");
            table[0] = 2;
        }
        return table;
    }

    unsigned int st = 522;
    if (encoding) st = 2100000; // We create a big table to contain all the UNICODE characters.
    unsigned long long int* t = calloc(st, sizeof(unsigned long long int));
    if (t == NULL)
    {
        static unsigned long long int table[1];
        printf("Error in wordlist_analyzer.dll :\n");
        printf("Allocation 1 of %u octets error", st*8);
        table[0] = 3;
        return table;
    }

    int end_separator=0; // Boolean indicating if there is a separator before EOF at the end of the file
    unsigned long long int minimum=-1, maximum=0, wordLength;
    unsigned long int min_code_point = -1;
    unsigned long int max_code_point = 0; // This variable will give the possibility to delete a part of the big array t.
    unsigned long int c;
    do
    {
        wordLength = -1; // Indeed, the separator is counted in the length of the word.
        do
        {
            if (encoding)
            {
                c = getc_utf8(f); // Multi-octets encoding UTF-8.
            }
            else
            {
                c = getc(f); // One octet encoding (ASCII, latin-x ...).
            }
            wordLength++;
            if (c != EOF)
            {
                if (!t[I_O_TABLE+c]) // If the character is new ...
                {
                    if (strchr(separators, c) == NULL) // If the character is not a separator
                    {
                        t[I_N_DIFF_CHAR] += 1; // Increasing the counter of different characters
                    }
                    if (c < min_code_point) min_code_point=c;
                    if (c > max_code_point) max_code_point=c;
                }
                t[I_O_TABLE+c] += 1; // Increasing the number of occurrences of the character c
            }
            else
            {
                break;
            }
        }
        while (strchr(separators, c) == NULL);

        if (wordLength < 255)
        {
            t[I_L_TABLE+wordLength] += 1;
        }
        else
        {
            t[I_L_TABLE+255] += 1;
        }
        if (wordLength < minimum)
        {
            if (wordLength)
            {
                minimum = wordLength;
            }
        }
        if (wordLength > maximum)
        {
            maximum = wordLength;
        }

    }
    while (c != EOF);

    t[I_SIZE_TABLE] = I_O_TABLE + max_code_point + 1;

    unsigned long long int* table = calloc(t[I_SIZE_TABLE], sizeof(unsigned long long int));
    if (t == NULL)
    {
        static unsigned long long int table[1];
        printf("Error in wordlist_analyzer.dll :\n");
        printf("Allocation 2 of %I64u octets error", t[I_SIZE_TABLE]*8);
        table[0] = 4;
        return table;
    }
    for (unsigned long int i=0 ; i < t[I_SIZE_TABLE] ; i++)
    {
        table[i] = t[i];
    }
    free(t);

    table[I_SIZE_FILE] = ftell(f); // The position of the cursor gives the size of the file.
    if (table[I_SIZE_FILE])
    {
        fseek(f, -1, SEEK_CUR);
        if (strchr(separators, getc(f)) != NULL)
        {
            table[I_L_TABLE] -= 1;
            end_separator = 1;
        }
        if (table[I_L_TABLE])
        {
            minimum = 0;
        }

    }
    fclose(f);

    table[I_L_SMALLER_WORD] = minimum;
    table[I_L_BIGGER_WORD] = maximum;
    table[I_MIN_CODE_POINT] = min_code_point;
    table[I_MAX_CODE_POINT] = max_code_point;
    if (!encoding)
    {
        table[I_N_CHAR] = table[I_SIZE_FILE]; // If a character is encoded in one octet, the number of characters and octets are equal.
    }
    else
    {
        table[I_N_CHAR] = 0; // Else we have to sum all the occurrences of all the characters.
        for (int i=I_O_TABLE ; i < table[I_SIZE_TABLE] ; i++)
        {
            table[I_N_CHAR] += table[i];
        }
    }
    table[I_N_WORDS] = 0;
    for (int i=I_L_TABLE ; i < I_L_TABLE+256 ; i++)
    {
        table[I_N_WORDS] += table[i];
    }
// Calculation of average * 1000 : M = (nchar - nseparators) / nwords * 1000 = (nchar - (nwords - 1 + end_separator)) / nwords * 1000 = (nchar - nwords + 1 - end_separator) / nwords * 1000 = (nchar + 1 - end_separator) / nwords - 1000
    if (table[I_N_WORDS])
    {
        table[I_AVERAGE_L_WORD] = (table[I_N_CHAR] + 1 - end_separator) * 1000 / table[I_N_WORDS] - 1000;
    }
    else
    {
        table[I_AVERAGE_L_WORD] = -1;
    }

    if (table[I_L_BIGGER_WORD] < 255) // We can easily calculate the inferior median
    {
        unsigned long long int m = (unsigned long long int) (table[I_N_WORDS]+1) / 2;
        unsigned long int a = 0;
        int i=I_L_TABLE ;
        while (a < m)
        {
            a += table[i++];
        }
        if (table[I_N_WORDS] % 2 == 1)
        {
            table[I_MEDIAN_L_WORD] = (i - 1 - I_L_TABLE) * 10;
        }
        else
        {
            table[I_MEDIAN_L_WORD] = (i - 1 - I_L_TABLE) * 10;
            while (table[i]==0)
            {
                i++;
            }
            table[I_MEDIAN_L_WORD] =  (unsigned long long int) (((float) (table[I_MEDIAN_L_WORD] + (i - I_L_TABLE) * 10)) /2);
        }
    }
    else
    {
        table[I_MEDIAN_L_WORD] = -1; // Else the median is not calculated
    }

    return table;
}
