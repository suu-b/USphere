MewTube V2 or USphere

## Story

Last year, I thought of creating a custom YouTube for myself. But after some work, the idea went nowhere and stalled. I lost my interest. Partly, because I wanted to apply ML to it - to rank videos - and it seemed too big a task. And partly because I didn’t believe the resultant product would be of any real utility.

## V2

But now, I think it would be a really intriguing thing to work on - the utility of the resultant doesn’t matter - I just want to see the whole model working.

## The Model

There are two models that I came up with:

### Video Pooling Model

Periodically, the system will collect metadata of videos. A list of topics will be seeded to the system; the LLM layer will generate high-impact search terms and search YouTube using YouTube’s Data API. It will collect the required metadata of these videos, deduplicate the batch, filter using some ‘criteria’, and dump them in a knowledge base.
The GUI client will hit the backend. The backend will fetch a batch of videos to show.
Now, based on my interaction with these videos - liking, watch time, etc.- the ML layer will rank them and adjust the ‘criteria’.

That will work in a loop.
This model may be crude because I didn’t develop much here. This is because the pool the

### Channel Pooling Model

Instead of relying on search terms, it relies on channels. A list of channels will be seeded to the system; the system will crawl their content and find channels they have collaborated with. It further crawls these newfound channels’ content and finds their collaborations.
In this way, a three-layered sphere will be created.
The innermost layer - the core - contains the seeded list of channels.
The middle layer - the mantle - contains the secondary list of channels (collaborations of the core).
The outermost layer - the crust - contains the tertiary list of channels (collaborations of the mantle).

The model makes two core assumptions -

1. User’s preferred value resides only in the seeded list of channels.
2. If the core channel has collaborated with another channel, the other channel is valuable as well. However, the model is a bit skeptic therefore, places it in a lower layer.

The system is charitable - based on user activity, it will allow channels to climb the layers from crust to core. Additionally, it will be cruel - it will sink channels to lower layers if their videos lose engagement. The system can even archive channels, meaning they wouldn’t exist in the sphere anymore but in archives for a possible revival.

The only shortcoming of the model is that it can form a bubble, a sort of saturation of ideas leaving no space for novelty. This is because of two reasons -

1. Since it begins from channels I watch, it is highly likely they will collaborate with channels like them only (sorta of the same team), which will form a bubble with no inlet of novel content.
2. There is really no inlet of new videos provided. Once the three layers are populated during the initial run, there is no way for new channels to come in. Surely, there is a way for existing channels to get archived tho.


Perhaps, we may need a fourth mechanism - **controlled exploration**. Periodically, we can sample channels existing outside the sphere, evaluate them, and admit a few in the crust. But again, controlled.

However, there is perhaps a more important distinction to make: that we may need a boundary between discovery, recommendation, and consumption. Discovery is about finding new content, recommendation is about suggesting user based on their projects or search, and consumption is about watching and engaging with the recommended content. 
Channel pooling is a model of discovery and intial placement in the sphere. We may optionally add controlled exploration to the stage as well.
We may need a recommendation model to suggest out of the current sphere.
Consumption is about engagement and how, based on that, the channels will be moved between the layers and recommendations be made.