#!/usr/bin/env python3
"""
Build words.js for Word Chain Infinity.

The game runs entirely in the browser (so it can be hosted free on GitHub Pages),
and this Python script prepares its data:

  * DICT    - every lowercase English word (used to validate player words)
  * NAMES   - proper nouns (people, places, brands) - allowed only when
              the "No proper names" rule is switched off
  * COMMON  - dictionary words ranked by how common they are (the AI's vocabulary;
              easy bots use the top of the list, hard bots use all of it)
  * CATS    - word lists for Category mode

Requirements:
    sudo apt install wamerican        # provides /usr/share/dict/american-english
    pip install wordfreq

Run:
    python3 build_words.py            # writes words.js next to this file
"""
import json
import re
from pathlib import Path

from wordfreq import top_n_list

SRC = Path("/usr/share/dict/american-english")
OUT = Path(__file__).with_name("words.js")

raw = SRC.read_text(encoding="utf-8").split()
dict_words = sorted({w for w in raw if re.fullmatch(r"[a-z]{2,}", w)})
dict_set = set(dict_words)
names = sorted({w.lower() for w in raw if re.fullmatch(r"[A-Z][a-z]{2,}", w)} - dict_set)

# Words the AI bots will never say (players can still use any real word).
BOT_BLOCKLIST = set("""
    anal anus arse ass asses bastard bitch bitches bitchy blowjob bollocks boner boob boobs butt
    butthole clit cock cocks coon crap cum cunt damn dick dicks dildo dyke fag faggot fags fanny
    fart feck fuck fucked fucker fucking gay goddamn hell homo horny jizz kike kinky lesbian nazi
    negro nigga nigger orgasm pecker penis piss pissed poop porn porno prick pube pussy queer rape
    raped rapist retard semen sex sexy shit shits shitty slut sluts smut spic suck sucks tit tits
    titty turd twat vagina wank wanker whore wop
""".split())
common = [w for w in top_n_list("en", 60000)
          if w in dict_set and len(w) >= 3 and w not in BOT_BLOCKLIST]

CATEGORIES = {
    "Animals": """aardvark albatross alligator alpaca anaconda angelfish ant anteater antelope ape armadillo
        baboon badger barracuda bat bear beaver bee beetle bison boar buffalo bull butterfly buzzard
        camel canary caribou cat caterpillar catfish cheetah chicken chimpanzee chinchilla chipmunk clam cobra
        cockroach cod condor cougar cow coyote crab crane crane cricket crocodile crow cuckoo deer dingo dog
        dolphin donkey dove dragonfly duck eagle eel egret elephant elk emu falcon ferret finch firefly
        flamingo flea fly fox frog gazelle gecko gerbil gibbon giraffe gnat gnu goat goldfish goose gopher
        gorilla grasshopper grouse gull hamster hare hawk hedgehog heron herring hippopotamus hornet horse
        hummingbird hyena ibis iguana impala jackal jaguar jellyfish kangaroo kingfisher kitten kiwi koala
        ladybug lamb lark lemming lemur leopard lion lizard llama lobster locust lynx macaw magpie mallard
        manatee mantis marmot meerkat mink mole mongoose monkey moose mosquito moth mouse mule narwhal newt
        nightingale ocelot octopus opossum orangutan oriole ostrich otter owl ox oyster panda panther parrot
        partridge peacock pelican penguin pheasant pig pigeon piranha platypus pony porcupine porpoise
        possum puffin puma python quail rabbit raccoon ram rat rattlesnake raven reindeer rhinoceros robin
        rooster salamander salmon sardine scorpion seahorse seal shark sheep shrew shrimp skunk sloth slug
        snail snake sparrow spider squid squirrel starfish stingray stork swallow swan tapir tarantula
        termite tiger toad tortoise toucan trout tuna turkey turtle viper vulture wallaby walrus wasp
        weasel whale wildcat wolf wolverine wombat woodpecker worm wren yak zebra""",
    "Food": """almond anchovy apple apricot artichoke asparagus avocado bacon bagel banana barley basil bean
        beef beet biscuit blueberry bread broccoli brownie burger burrito butter cabbage cake candy cantaloupe
        caramel carrot cashew cauliflower celery cereal cheese cherry chicken chili chips chocolate chutney
        cinnamon clove coconut coffee cookie corn cracker cranberry cream croissant cucumber cupcake curry
        custard date dough doughnut dumpling egg eggplant fig fish flour fudge garlic ginger grape grapefruit
        gravy guava ham hazelnut honey hotdog hummus icing jam jelly juice kale ketchup kiwi lasagna lemon
        lentil lettuce lime lobster macaroni mango maple margarine marmalade mayonnaise meatball melon milk
        mint muffin mushroom mustard noodle nougat nutmeg oat oatmeal olive omelet onion orange oregano
        pancake papaya paprika parsley pasta pastry peach peanut pear pepper pickle pie pineapple pistachio
        pizza plum popcorn pork porridge potato pretzel pudding pumpkin quiche radish raisin raspberry rice
        risotto roll salad salami salmon salsa salt sandwich sausage soup spaghetti spinach squash steak stew
        strawberry sugar sushi syrup taco tangerine tea toast tofu tomato tortilla truffle tuna turnip
        vanilla vinegar waffle walnut watermelon wheat yam yogurt zucchini""",
    "Nature": """avalanche bark bay beach blizzard blossom boulder branch breeze brook bush canyon cave cliff
        cloud coast comet coral cove crater creek dawn delta desert dew drizzle dune dusk earth earthquake
        eclipse estuary fern field fjord flood flower fog forest fossil frost galaxy geyser glacier gorge
        grass grove gulf hail harbor heath hill horizon hurricane ice iceberg island isthmus jungle lagoon
        lake lava leaf lightning marsh meadow mist monsoon moon moss mountain mud nebula oak oasis ocean
        orbit pebble peak pine planet plateau pond prairie puddle rain rainbow rainforest ravine reef ridge
        river rock root sand savanna sea seed shore sky sleet snow soil spring star stone storm stream summit
        sun sunrise sunset swamp thunder tide tornado tree tundra twig typhoon valley vine volcano waterfall
        wave weed willow wind wood""",
    "Home": """armchair attic balcony basement basin bath bathtub bed bedroom bench blanket blender book
        bookcase bottle bowl broom brush bucket cabinet candle carpet ceiling chair chimney clock closet
        couch cup cupboard curtain cushion desk dishwasher door doorbell drawer dresser duvet fan faucet
        fence fireplace floor fork freezer fridge furnace garage garden gate glass hallway hammer hanger
        heater hook iron jar kettle key kitchen knife ladder lamp lantern laundry lock mailbox mat mattress
        microwave mirror mop mug napkin needle oven pan pantry pillow plate porch pot quilt radio rake roof
        rug saucepan saucer scissors shelf shower sink sofa spatula sponge spoon stairs stool stove table
        teapot television toaster toilet towel tray vacuum vase wall wardrobe window yard""",
    "Jobs": """accountant actor architect artist astronaut athlete author baker banker barber bartender
        biologist blacksmith butcher captain carpenter cashier chef chemist cleaner clerk coach cook
        dancer dentist designer detective developer diver doctor driver economist editor electrician
        engineer farmer firefighter fisherman florist gardener geologist guard guide hairdresser historian
        inspector instructor janitor jeweler journalist judge lawyer lecturer librarian lifeguard locksmith
        magician manager mason mechanic midwife miner model musician nanny navigator nurse optician painter
        paramedic pharmacist photographer physician physicist pilot plumber poet police politician porter
        postman potter professor programmer psychologist publisher receptionist reporter researcher sailor
        salesman scientist sculptor secretary senator servant sheriff singer soldier surgeon surveyor tailor
        teacher technician therapist translator tutor umpire vendor veterinarian waiter waitress welder
        writer zookeeper""",
    "Sports": """archery athletics badminton ball baseball basket basketball bat bicycle bowling boxing
        canoe captain catch champion chess climbing coach cricket croquet curling cycling dart diving dodgeball
        dribble fencing field football gloves goal golf gym gymnastics hammer handball helmet hockey hurdle
        javelin jogging judo karate kayak kick lacrosse league marathon match medal net offside olympics
        paddle pitch polo pool puck quarterback race racket referee relay rowing rugby running sailing
        score skate skating ski skiing sled snooker snowboard soccer softball sprint squash stadium surfing
        swimming team tennis throw touchdown track trophy umpire volleyball wicket windsurfing wrestling yoga""",
}
cats = {}
for name, blob in CATEGORIES.items():
    words = sorted({w for w in blob.split() if w in dict_set})
    cats[name] = " ".join(words)
    print(f"{name}: {len(words)} words")

js = (
    "// Generated by build_words.py - do not edit by hand.\n"
    f"window.WC_DATA={{dict:{json.dumps(' '.join(dict_words))},\n"
    f"names:{json.dumps(' '.join(names))},\n"
    f"common:{json.dumps(' '.join(common))},\n"
    f"cats:{json.dumps(cats)}}};\n"
)
OUT.write_text(js, encoding="utf-8")
print(f"dict={len(dict_words)} names={len(names)} common={len(common)} -> {OUT} ({OUT.stat().st_size//1024} KB)")
