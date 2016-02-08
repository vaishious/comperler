int strCmp(char *s1,char *s2)
{
    int i;
    for(i = 0;s1[i] || s2[i];i++) {	// Only end if both strings terminate 
        if(s1[i] > s2[i]) {    
                return 1;
        } else if(s1[i] < s2[i]) {
                return -1;
        }
    }
    return 0; // Will only reach here if both have same length and same characters at all points
}
