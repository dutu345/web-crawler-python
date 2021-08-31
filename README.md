# web-crawler-python
A web crawler made with Beautifulsoup which extracts emails and contact phones from a given list. It converses the web page to text, where it first extracts 
with regexp the matching phone numbers and emails. Then, the crawler checks if there is any url+"/contact" page, where it tries to extract again the matching phones and emails.
(Lots of comments remained from previous debugging.) 
