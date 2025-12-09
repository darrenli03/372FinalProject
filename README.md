# CS372 Final Project

## What it Does

This project is a retrieval-augmented generation (RAG) pipeline that creates embeddings from the Commerce Control List (pdf available for download at https://www.ecfr.gov/current/title-15/subtitle-B/chapter-VII/subchapter-C/part-774/appendix-Supplement%20No.%201%20to%20Part%20774), then uses those embeddings to decide whether user-provided products/components (for example: ceramic body armor plates) are restricted or not. Future plans include multi-component processing via excel and including the ITAR in the embeddings.

## Quick Start (Developers)

- **Backend (PowerShell):** create and activate a Python virtualenv, install backend requirements, then run the server:

```
python -m venv .venv_new; .\.venv_new\Scripts\Activate.ps1
pip install -r backend\requirements.txt
python backend\server.py
```

- **Frontend (PowerShell):** install node modules and start the dev server from the `frontend` folder:
  - Note: you will have to change the fetch endpoint in [App.jsx](https://github.com/darrenli03/372FinalProject/blob/main/frontend/src/App.jsx) to the localhost endpoint: "http://127.0.0.1:8080/query_single?search_query=${encoded}" 

```
cd frontend; npm install; npm run dev
```
For more details, check out `SETUP.md`

## Video Links

- Non-technical demo video: [linked here](https://youtu.be/20f0HVoEuMw)
- Technical walkthrough: [linked here](https://youtu.be/eLkqJT3o3_U)

## Evaluation

- Testing Datanbase: https://docs.google.com/spreadsheets/d/1KOmhZdAN5oiNj53-cfMunaYKK5Qf9fVJdLKmyaLzLyc/edit?usp=sharing 

Summary:
- Quantitative:
  -  Model correctly identified 47/52
  - Overall accuracy of 90.4% 
  - Precision: Model had a precision of 100% for “Yes” and a precision of 84.4% for “No”
  - Recall: Model’s 25 expected “Yes” responses, it only gave us 20 so we have a recall of 80%

- Qualitative:
  - Edge cases technically correct and also explains chain of thought and justifies anwser in anwser return section
  - Retrevied context almost always contains queried item when model is correct and often misses it when model is wrong

Full Analysis:
  The main objective of our project was to build a system that businesses can reliably use to check if their items are CCL compliant. In our testing dataset, we picked 25 random items from the CCL index and used the corresponding CCL text as the “Golden Context.” We then picked 25 non-restricted items and 2 edge cases to test the model’s accuracy. For items that are restricted, we also wanted to compare the context returned by the model to the “Golden Context” recommended by the CCL Index. 
  
  Out of the 25 restricted items, the model correctly identified 20 items as restricted and incorrectly identified 5 as unrestricted. When we tested it on the unrestricted items, it correctly identified all 25 as unrestricted. Lastly, when we tested our edge cases of “Germany” and “Joe Biden”, the model returned a final recommendation of “No”, but did state that “The query presented is "Joe Biden," which does not refer to a product, component, or technical description relevant to export control compliance. There are no key technical characteristics associated with this name that can be analyzed against the Commerce Control List (CCL) or any export control criteria. Since the CONTEXT does not provide any information or classifications regarding a person, it cannot be associated with any thresholds, performance parameters, material specifications, or definitions relevant to the CCL.” when prompted with “Joe Biden”, and returned “The query is simply "Germany," which does not provide any technical characteristics, product specifications, or descriptions that can be classified under export control regulations. The provided CONTEXT describes specific items controlled under the U.S. Commerce Control List (CCL) related to silicon, germanium, rhenium, and other materials, along with specific thresholds and requirements. However, the query does not pertain to a product, component, or technical description as required for classification under the CCL. It simply mentions a country, which does not meet the criteria for classification in the context provided.” when prompted with “Germany”. Interestingly enough, the model did search for the closest thing to our edge cases, which was Germanium for Germany and the model was unable to find anything for Joe Biden. We view this as an acceptable result since while impossible to export, there technically is nothing in the CCL that prevents the export of these two items and the model does warn the user that these are not products of items contained in the CCL. We conclude that our model correctly identified 47/52 and has an overall accuracy of 90.4%. When it comes to precision, 100% of the model’s “Yes” responses were correct and 27/32 of the model’s “No” responses were accurate meaning the model had a precision of 100% for “Yes” and a precision of 84.4% for “No”. Lastly, our of the model’s 25 expected “Yes” responses, it only gave us 20 so we have a recall of 80%.

  Now that we have covered the quantitative metrics, let's analyze the qualitative ones. For this section, I want to analyze how close the returned context was to the Golden Context. Interestingly enough, one of the key things I noticed was that sometimes, the returned context would not even include the key word itself! The five items the model incorrectly classified as non-restricted were: Yellow fever virus, Yttrium oxide crucibles, Zinc germanium biphosphide, Technology for diamond substrate, and Potassium titanyl arsenate. Out of these 5, the key word itself was mentioned in almost all of the Golden contexts (with the exception of yttrium oxide crucibles where the two were mentioned separately), but 3 out of the 4 returned contexts did not even include the word itself! For example, the Golden context for Yellow Fever Virus refers to section 1C351.a.58 which explicitly mentions Yellow Fever, but the returned context covers 1C351.a.4 to 1C351.a.53 and seems to miss 1C351.a.58, thus not covering Yellow Fever Virus. Another example could be Zinc Germanium Phosphate where it is directly mentioned in its Golden context, section 6C004.b. While the returned context does briefly mention “Non-linear optical materials, other than those specified by 6C004.b”, it again seems to miss the actual context itself. It seems that most of the time, when the model returns the wrong answer, it might be because it is referring to a similar, but not accurate segment of text. To future verify this, I also compared the returned contexts to the Golden Contexts when the model was correct. I found that when the model was able to correctly predict if an item was restricted and the item itself was explicitly named in the Golden context, it was almost always found in the returned context as well. This suggests that a main driver behind wrong predictions could be that the model is simply not picking the right pieces of context at times.  


## Individual Contributions

- Darren Li
  - Backend: RAG pipeline `doc_embedding.py`, including Pinecone vector store integration (`pinecone_upload.py`), OpenAI integration (`gpt_query.py`) and server API endpoints (`server.py`)
  - Frontend: React app and UI (`frontend/src` components) implementation and integration with backend API
  - Additional work: Setting up AWS EC2 instance (Nginx and HTTPS certificate configuration), deploying frontend on Vercel (DNS configuration) with DoS protection via Cloudflare
- Andy Li
  - PDF processing (`text_extractor.py`)
  - Testing dataset curation [linked here](https://docs.google.com/spreadsheets/d/1KOmhZdAN5oiNj53-cfMunaYKK5Qf9fVJdLKmyaLzLyc/edit?usp=sharing)
  - Manual testing of model performance for items in testing dataset 
  - Analyzing results quantitatively and qualitatively

## Miscellaneous Notes

- Could also implement a chat mode in addition to the automated excel sheet processing, that can get us this rubric item:
  - Built multi-turn conversation system with context management and history tracking (7 pts)
- fine tuning would require significant effort since we need to create the prompt/answer database ourselves
- To regenerate the database, boot up the virtual environment with the requirements from backend/requirements.txt, first run doc_embedding.py (text_extractor.py generated files/ccl.txt that is already version controlled, but may need to be updated as the legal body updates) (this will likely take an hour or two), then run pinecone_upload.py to replace the old index in pinecone with the new embeddings (perhaps about 10 minutes?)
