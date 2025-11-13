# Development Spec

I would like to create a text editing utility for the Linux desktop whose focus is on applying templated edits to text using an LLM (API: Open Router; default model ).

I have created, previously, a list of text transformation templates and have cloned them at /prompts. These are intended for use as system prompts: the body text is the user prompt and they get sent to the API for completion. Typically the minimum temperature is used. On modern models, this approach works very reliably. I have listed a few Open Router models in models.md that I'd like to offer as options with openai/gpt-5-mini as default.

Here's the UI I'm envisioning for the target distro - Ubuntu.

A basic plain text editor (perhaps a project could be forked as a jumpstart?). I'm on KDE and use Kate but could just as well use something far simpler. For now - consider even spellcheck a "down the line" feature.

From my prompt library there are a few text transformations that I use all the time.

Note: These are intended as markdown to markown editing instructions: the user provides markdown and the AI returns it

- Voice note cleanup: a basic cleanup instruction to take the text knowing that it's a voice note and add what's missing: puncutation, paragraph breaks 

Formatting transformations:

-> Format this text as an email 
-> As a blog post 
-> As a social media post 
-> As a blog outline 
-> As an RFP 
-> As a bug report 
-> As a feature request 
-> As a Reddit post 

Each one of these prescribes in very simple terms the expected format, although I expect that it can be inferred. For Reddit I might say: "format this as a casual and friendly post for sharing on a subreddit." 

Stylistic transformations:

-> Business to casual 
-> Casual to business 
-> Formal to informal 
-> Informal to formal 

Word count: expansion and truncation 

-> Fill up to  word count 
-> Reduce to word count  

Specific style instructions

-> Add metaphors 
-> Reduce metaphors 
-> Make more simple 
-> Use simpler sentence structure 
-> Break up long paras 

Formatting (of text);

-> Add subheadings 
-> Add subheadings, bold 
-> Move all links to end 

Gramattical transformers:

-> First to third person 
-> Third to first 
-> Past to present 
-> Present to past 

Style guide conformity 

-> CMS 

UK English variant conformity 

-> UK English
-> US English 
Etc 

For fun but also sometimes useful:

-> Make super hyerbolic  
-> Make this text read like a cheesy direct sales campaign ad 
-> Make this text Shakespearean 
-> Use archaic vocab 
-> Add random foreign words 
-> Make this as complicated and possible 
-> Format this in the style of a telegram from another century 
-> Stuff with platitudes 
-> Make painfully inspirational 
-> Format as humblebrag 

Ones I've drafted on principle because I think it's a powerful use-case:

- Obfuscation (for whistleblowing etc, obfuscates names and places) 

Partial list - there are literally hundreds of ways in which text can be changed!

# UI Considerations 

The challenge I think is to make this useful without making it very complicated. 

Here are the features I'd like

## Select + transform 

Select all + select transforms = it  will transform all the text 

Select text freehand then right click ten select transform this text - only highlighted text gets sent to LLM for transform 

# Transformation Logic 

Sometimes text edits work great. Sometimes LLMs butcher text between versions. So falling back through a sequence of versions is very important. 

I have no firm idea as to what is the best way to achieve this so I leave this up to you: perhaps the answer is temporary in-app memory as otherwise, for true versioning, we're looking at a more elaborate backend and having to save files locally (I think!). Neither are desirable from my perspective: the use I'd make of this is as a quick and handy text editing utility to run these quickly on pasted text and then paste somewhere else - so retention at source is not a big priority. 

But if we can implement a lightweight version logic: arrows for next and previous version (e.g. back one iteration, forward one iteration, restore original).

## Split pane nav 

Left = original text, right = transformed text. 

The left pane updates as one progresses through versions. After the first transform the right pane is the latest / leading version of the text and can be edited freehand. 

THIS text gets sent on sequential edits, which can also be "all text" (default) or select only this text with context menu. 


Button for "New" to start a fresh editing job

Finally:

- copy to clipboard button 
- download button (downloads latest transformation as markdown to desktop, filename = timestamp)

---

# Text Transforms 

Text transforms are loaded in the app's backend and can be selected using a top bar navigation which organised them by category. There's also a freeform search so you can search for a transform. 

Up to 5 transformations can be used simultaneously.

The backend logic is:

Latest text (original on first run, latest on subsequents) + system prompt + brief preface + concatenated instructions     sent to LLM API 

The preface might be:

"Please apply the following list of edits to the text" - and then each loaded transformation prompt separated with horizontal line to make separation easier to parse. 

# Memory And Backend

Backend will need to store persistently: API key, model preference, transformation data array. 

Consider either implementation viable; choose whichever you think makes the most sense for a local GUI: SQLite, file-based memory (JSON etc). 

# Build And Deployment Process

I'm building this for my own use but am open sourcing the project. I like to share the outputs. I'm on Ubuntu so a .deb is preferred. 

The following scripts help me to build and iterate quickly:

- build script 
- gitignore exceptions for build artefacts 
- update script to rebuild from source and make sure version number is properly updated between versions 

# Custom Transformations 

Feature for iteration two: the ability for the user to create their own transform prompts and save them into the library and perform CRUD ops on the transform store in general including ordering them into folders (app ships with default backend and user can customise to suit their own needs). 

Best implementation: prompt management screen. Do not attempt to crowd too much into one part of the UI.

# User Detail Store 

In general the text transform approach works very well. However, one limitation is that without supplementary data, it won't know who I am.

If I want to, say, format a voice note into an  email it will have to end:

Regards,
(Your Name)

Which is unfortunate as it might otherwise have got me to the finished product!

I've thought about a workaround which is the ability for the app to store some basic info about you like name and email with the idea that this data could be loaded into the prompt constructor. 

So the email formatting prompt might be:

System Prompt + 
Text transform prompt + 
User details + 
Text 

To receive:

Formatted email with user's signature already applied. 

This customisation logic could be applied for every prompt ("customise using these details if necessary") or injected more selectively to prevent needlessly including non-helpful context in situations where it doesn't apply.

# General Guidance 

What I'm trying to create: something quick versatile and easy to use 