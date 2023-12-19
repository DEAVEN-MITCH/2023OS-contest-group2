#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <assert.h>
#include <unistd.h>

#define ASSERT assert

int *readFile(int d, int *numHashes)
{
   int l;
   int pages, bytesPerPage;
   int *hashes = NULL;
   char buf[2048];
   int loc = 0;
   int i;
   int num;

   while(1) {
      lseek(d, loc, SEEK_SET);
      num = read(d, (char*)&buf, 1024);

      if (num < 1) {
         printf("Failed to locate hash string in file.\n");
         return NULL;
      }

      buf[num] = '\0';

      l = sscanf(buf,"Hash:%d:%d:", &pages, &bytesPerPage);

      if (l != 2) {
         i = 0;
         while(buf[i] != '\0' && buf[i] != '\n') {
            i++;
         }

         while(buf[i] == '\n' || buf[i] == '\r') {
            i++;
         }

         loc += i;
         continue;
      }

      i = 0;
      while(buf[i] != ':') i++;
      i++;
      while(buf[i] != ':') i++;
      i++;
      while(buf[i] != ':') i++;
      i++; // Skip to end of hash intro
      loc += i;
      break;
   }

   *numHashes = pages;

   {
#ifndef NOSANITY
      int newloc;
      int endloc;

      newloc = lseek(d, loc, SEEK_SET);
      endloc = lseek(d, 0 - ((pages*bytesPerPage)+1), SEEK_END);

      /*
       * At this point, we'd like to try to confirm that our hashlists aren't
       * corrupt.  Best we can do is ensure that the list appears to end after
       * the proper number of bytes.  So, check for EOF where we think it
       * should be, or for a bloomfilter start entry.  Define NOSANITY to
       * disable sanity checking.
       */
      if (newloc != endloc) {
         lseek(d, loc + ((pages*bytesPerPage)+1), SEEK_SET);
         num = read(d, (char*)&buf, 1024);

         if (num > 32) {
            l = sscanf(buf,"BloomFilter:%d:", &num);

            if (l > 0) {
               goto sane;
            }
         }

         printf("File doesn't end immediately after hash list.  Hash list may be corrupt, or file may contain extra data (bloom filter, for example).  Either way, aborting.\n");
         return NULL;
      }
sane:
#endif

      lseek(d, 0, SEEK_SET);
   }

   {
      char * tmp;

      tmp = (char*)mmap(NULL, loc+(pages*bytesPerPage), PROT_READ, MAP_SHARED, d, 0);

      if (tmp != NULL) {
         hashes = (int*)(tmp + loc);
      }
   }

   return hashes;
}

int main(int argc, char ** argv)
{
   int d1;
   int *hashes1, numHashes1;
   int i;

   if (argc != 2) {
      printf("Syntax: %s [file1]\n", argv[0]);
      exit(0);
   }

   d1 = open(argv[1], O_RDONLY);

   if (d1 == -1) {
      printf("Couldn't open %s for reading.\n", argv[1]);
      exit(0);
   }

   hashes1 = readFile(d1, &numHashes1);

   if (hashes1 == NULL) {
      printf("Error reading hashes from %s\n", argv[1]);
      exit(0);
   }

   for (i = 0; i < numHashes1; i++) {
      printf("%X\n", hashes1[i]);
   }

   close(d1);

   return 1;
}