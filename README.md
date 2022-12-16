# Text Processing

Working with a large collection of different texts can be time-consuming and difficult. It's interesting to find ways to summarize them and look for easy ways to perform searches quickly. In this context, this repository contains some options that deal with the application of some methods that facilitate the process of discovering information in large collections of texts, such as: pre-processing treatments, identification of words with the highest number of occurrences, inverted index, searches and ranking. All scripts were developed using the Python programming language.

Regarding the database, 143 texts were used in .htm format that can be found in the Dataset folder present in this repository. All texts are written in Portuguese.

## Preprocessing

Some existing problems were identified in the texts that had to be addressed so that they did not affect the results. They were:

- Existence of identification of a narrator A at the beginning of some lines;
- Existence of identification of a narrator X at the beginning of some lines;
- Existence of some HTML tags;
- Existence of special characters;
- Existence of conversion of accents and ç to terms (tilde, acute, grave, cedil).

The permanence of such terms and characters in the texts could harm the results, so they were duly removed.

## Script 01: Identification of words with the highest number of occurrences

Here the objective was to identify the 10 words that appear most in all texts and present them in descending order with the number of occurrences.

Remember to change the location directory of the collection of texts, so that you can find them on your computer.

In this script, each text is opened one at a time, so that they are treated by the removeLixo() function and each word is counted by the Counter, which can take a little longer. The Counter is responsible for storing each identified word in the texts and saving the number of occurrences of each one of them. It then prints out the top 10 most frequently occurring words, as follows:

- 775: pois
- 578: assim
- 465: dizer
- 460: aqui
- 426: sim
- 426: tambe
- 416: quer
- 365: coisa
- 353: ate
- 345: agora

For the collection of texts used, the word with the highest number of occurrences is POIS, with 775 occurrences.

As a complement, a graph is also printed that demonstrates the relationship between the 10 words and the number of times they appear.

<p align="center">
<img width="400" src="/Figures/01.png" alt="Figure 01">
</p>

## Script 02: Inverted Index and search by query

The Inverted Index is nothing more than the presentation of each existing word in the texts and the designation of which text they appear. So with the Inverted Index, we have a simpler way to identify where to look for specific words.

As previously done, the texts are pre-processed.

Based on the result, a .pkl file is created with the Inverted Index and the Normal Word Index, in which the occurrence of words in each text is shown. To save the .pkl document, there must be a folder called obj in the same directory as the code script.

<p align="center">
<img width="700" src="/Figures/02.png" alt="Figure 02">
</p>

## Script 03: Vector Model and Ranking

In this application the objective was to implement structures and operations to provide information retrieval based on the Vectorial Model and Ranking. The system returns documents ordered from most relevant to least relevant to user queries. The sorting of results is in descending order.

In this case, only the 10 most relevant texts are printed, to avoid excessive information being displayed.

For example, for the term POIS, the following result is displayed:

<p align="center">
<img width="300" src="/Figures/03.png" alt="Figure 03">
</p>

The score indicates the relevance of the text to the search term. To search terms, simply change the value of the search_terms variable on line 51.

## Script 04: Modelo Probabilístico e Ranking

This last application has the same objective as the previous one, but using another model for classifying texts.

For the same term POIS previously researched, it is observed that the result was a little different. To search for terms, simply change the value of the search_terms parameter on line 277.

<p align="center">
<img width="600" src="/Figures/04.png" alt="Figure 04">
</p>

The documents belonging to the Top 10 remain almost the same, with only 2 divergences between documents. Another difference is in the position of each text in the Top 10. However, despite these divergences, it can be said that both models achieved similar performance.

## Conclusion

Here, some techniques for recovering information in collections of texts were presented in order to facilitate searches, regardless of what they are. Other methods exist, so it is important to research the applicability of each one and identify which one best suits the proposed problem. As it was possible to observe, two ranking models were applied. Although the results are very similar, differences can affect the conclusion to be obtained. therefore, it is important to thoroughly analyze the results to identify which best fits the proposed problem.
