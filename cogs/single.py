from collections import namedtuple
from discord.ext import commands
from discord.ext.commands import Context, Bot
from data import dbconn
from utils import cf_api, discord_, codeforces
from constants import LOWER_RATING, UPPER_RATING, RANGE, QUESTIONS

class Single(commands.Cog):
    def __init__(self, client: Bot):
        self.client = client
        self.db = dbconn.DbConn()
        self.cf = cf_api.CodeforcesAPI()

    @commands.group(brief='Commands related to single. Type .single for more details', invoke_without_command=True)
    async def single(self, ctx: Context):
        await ctx.send(embed=self.make_match_embed(ctx))

    @single.command(brief="Pratice on single mode")
    async def challenge(self, ctx: Context, rating: int):
        if not self.db.get_handle(ctx.guild.id, ctx.author.id):
            await discord_.send_message(ctx, "Set your handle first before challenging someone")
            return
        if rating not in range(LOWER_RATING, UPPER_RATING - RANGE + 1):
            await discord_.send_message(ctx, f"Invalid Rating Range, enter an integer between {LOWER_RATING}-{UPPER_RATING-RANGE}")
            return
        rating = rating - rating % 100
        handle = self.db.get_handle(ctx.guild.id, ctx.author.id)
        problems = await codeforces.find_problems([handle], [rating + i*100 for i in range(0, QUESTIONS)])
        Single = namedtuple('Single', 'guild p1_id rating problems status')
        await ctx.send(embed=discord_.single_problems_embed(Single(ctx.guild.id, ctx.author.id, rating, ' '.join([f"{x.id}/{x.index}" for x in problems[1]]), "0"*QUESTIONS)))

async def setup(client: Bot):
   await client.add_cog(Single(client))