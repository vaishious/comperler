/*int strCmp(char *s1,char *s2)*/
/*{*/
    /*int i;*/
    /*for(i = 0;s1[i] || s2[i];i++) {	// Only end if both strings terminate */
         If the next character of any one string is more in value than that of another then return 1, -1 appropriately
        /*if(s1[i] > s2[i]) {    */
                /*return 1;*/
        /*} else if(s1[i] < s2[i]) {*/
                /*return -1;*/
        /*}*/
    /*}*/
    /*return 0; // Will only reach here if both have same length and same characters at all points*/
/*}*/
int strCmp(char *str1, char *str2)
{
    while ((*str1 == *str2) && (*str1 != '\0'))
    {
        str1++;
        str2++;
    }
 
    if (*str1 > *str2)
        return 1;
 
    if (*str1 < *str2)
        return -1;
 
    return 0;
}
