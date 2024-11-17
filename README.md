# LoncaScraper
## Hi!

Thank you for your efforts when preparing the case. 

When providing a solution, I made some decisions, which I will try to explain below.

First of all, I needed to decide which libraries to use. I decided these libraries by priotrizing followings:

    [1] beanie, Object oriented approach, for the connection between MongoDB and Python.

    [2] lxml, becase we operate in near real time, it is one of the fastest libraries providing async functionality.

I used to deserialize an XML file using object-mapping approach but for this case (we need to be fast) and tech stack (Python), i used lxml.  

Secondly, there are some inconsistincies between given XML file and the PDF document. For example, there is not any model_measurements tag in the XML file although it is present in the documen or there is not ProductId while it is present in the XML file.

At this point, I decided to go by covering both of them, leaving doors open for inconsistent fields to be nullable in DB, so in this way I now can guarantee that any XML file either following both approach will be scraped succesfully into DB. 

Lastly, thank you again!! I enjoyed it when trying to provide a solution.

I will be waiting for your feedback.