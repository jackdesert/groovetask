#! /usr/bin/env python
# This file has some of the many textual messages

def introduction():
    output = why_groove_task() + q_n_a() + news() + references() + contact()
    return(output)

def why_groove_task():
    html = """
    <h2>Why GrooveTask?</h2>
    <p>You've been there. That morning when you woke up and couldn't look that treadmill in the face again if it were the last face on Earth. Or that afternoon when you were still hell-bent on putting that thesis together, but after six hours straight could no longer find the brainpower. So you kept at it, thrashing your own perfect grammar until it was a lifeless pile of characters in front of you that moved no one. Or those days when you were so deliciously productive that you forgot to call your mother and invite her to dinner until she was already cooking her own. And lastly, those weekends when you spent two whole days piddling around, dreading your homework. Later you realized you could have jumped right in, knocked out the hour or two that was necessary, and moved on to more meaningful things. But alas, that was later.
    </p><p>
    Yes, you've been there. Wondering why things didn't happen more naturally. You've stared up at the stars asking, "What shall I do.. and when?" Realizing that something was lacking in your life, you may have invested a small chunk of your life savings on a pencil. This pencil happily made a list for you of everything you'd like to do the next day. With vim and vigor it pressed itself into the pad, vowing that you'd have a productive day for its efforts. Surprisingly, upon waking you spent all morning on the two most pleasant, most meaningless things on the list (checking your facebook messages and tryout out a new chocolate chip cookie recipe), for which the pencil rewarded you two dime-sized smiley faces instead of checkmarks. Feeling guilty that you hadn't done more already, you plunged your afternoon into that marketing proposal your boss wanted you to put together this week. But your energy quickly faded, and your cells were grasping at straws. While you had been fresh in the morning, you had squandered your precious resources on those damned cookies. Now you needed every last wit of your brain power and it just wasn't there.
    </p><p>
    Ouch. Those days hurt. Miffed at the pencil for doing you in, you bought a day planner and a ball-point pen. "I'll keep all my life organized right here," you said aloud. You wrote and wrote in it-- sometimes cursive, sometime print-- but then you plunged off and did whatever you felt like anyway.
    </p><p>
    Perhaps you had been too stingy in your approach, you thought to yourself. So your next purchase was a Blackberry Smart Phone, thinking the added expense would pull more weight in your life and you'd actually pay attention to it for once. And the first two hundred and fifty times it beeped at you-- you did pay attention. But you're smarter than that now. While a Blackberry might have swell intentions, you're positive that it has absolutely no clue about how you're feeling at the moment. I mean, every morning at 9:06 am it beeps at you to write a letter to your uncle's second cousin Roger, and you don't dare take it off your schedule because you promised you'd write, but you're soon coming to grips with the idea that you JUST DON'T WANT TO. Doesn't it get it!?
    </p><p>
    Ah, so what are you missing now? Somewhere along the line you maybe realized that NOT ALL TASKS ARE WORTH DOING. Perhaps you realized that what you need is a way to manage your energy, not your time, and manage your important tasks well. The unimportant tasks are, well, not important. But there are a few key tasks that if done in a stellar manner, will propel you forth on your journey, receiving raises and promotions and fun.[1]
    </p><p>
    So your friend Jack, or maybe one of Jack's friends, or maybe one of Jack's friends' friends, referred you to this website named GrooveTask. And here you are, wondering what possible difference some lame website is gonna' make in your life. Well let me explain..
    </p><p>
    At GrooveTask, you get to decide what kind of groove you're in. What type of energy you are feeling.
    GrooveTask helps you prioritize your tasks for each kind of groove. It's okay if you don't get everything done that you set out to accomplish. I mean, I set out to be president of the United States. And I haven't gotten around to it yet, but I have accomplished several other, far more important things during this short lifetime..
    GrooveTask reminds you how long you want to spend (or not spend) on a particular task so you can get around to all the important ones.
    Most importantly, at GrooveTask I ask that you to listen to your body, your mind-- instead of the clock.
    </p>
    <h2>Getting Started with GrooveTask</h2>
    <ol>
    <li>Create an account using the \"Register\" button.It will automatically log you in.</li>
    <li>Read the descriptions of the three different grooves that GrooveTask offers.</li>
    <li>Make a list of your most important tasks, and file them under the most appropriate groove.</li>
    <li>Put the most imporant tasks from a given list at the top of that list. </li>
    <li>When you're ready to begin working on your tasks, Find the section labeled \"Go to Work!\" and click the groove you're in.</li>
    </ol>

    """
    return(html)



def q_n_a():
    html = """<h2>Q and A</h2>\n
    <p>Q: When I clicked on the "Add a Task" button, why does it just take me to the login page?<br>
    A: Make sure your browser has cookies enabled. If they're not enabled, it will forget that you're the one logged in.</p>
    <p>Q: I marked a task as available from 6:30 to 9:00, and it's 6:45 right now and it's not showing up. What gives?<br>
    A: This site is running on 24-hour time, so if you mean 6:30 <i>p.m.</i>, type in 18:30. Also check to see you're set
    to the time zone you think you're set to. As of January 10, 2010 all new users default to Eastern Standard Time (-5).
    Email the webmaster to have yours changed.

    """
    return(html)

def references():
    html = """
     <h2>References</h2>
    <ol>
    <li>Brian Tracy, <i>Eat That Frog!</i></li>
    <li>Elaine St. James, <i>Simplify Your Life</i></li>
    <li>Jim Loehr and Tony Schwartz, <i>The Power of Full Engagement</i></li>

    </ol>
    """
    return(html)

def news():
    html = """<h2>What's New</h2>
        <ul>
        <li>January 10, 2010-- Each user now can be on her own time zone. Email the webmaster to have your timezone changed.
        The current time and timezone are displayed when you 'Go to Work'. The news list was also changed so the newest stuff
        is at the top. </li>
        <li>January 8, 2010-- Support for utf-8 character sets, including the Spanish n with the ~ on it.</li>
        <li>January 4, 2010-- Changed everything to Eastern Standard Time</li>
        <li>November 10, 2009-- 'Clean Slate' buttons added to easily clear a task list.</li>
        <li>November 6, 2009-- All core features are now functional.</li>
        <li>November 6, 2009-- Tasks entered as "Start at exactly 3:00" now pop up at exactly 3:00
        (regardless of which groove they are listed under). For best results use this feature sparingly,
        only for things that can't be "grooved".</li>
        <li>November 5, 2009-- Tasks only show up during their marked 'available' time. Everything is in 24-hour Mountain Standard time. Also added a link to contact the system administrator, Jack</li>
        <li>November 3, 2009-- New introduction posted on login page</li>
        <li>November 2, 2009-- Website announced to friends and family</li>
        <li>November 1, 2009-- Tells you when you've spent too much time on the task</li>
        <li>Fall 2009-- Site goes live with the acquisition of the domains GrooveTask.org and GrooveTask.com</li>
        </ul> """
    return(html)

def contact():
    html = """<h2>Getting Help</h2>
        Fan mail, suggestions, questions, and comments about this website can be directed to
        <a href=mailto:jackdesert556@gmail.com?subject=Why_I_Love_GrooveTask>Jack</a> """
    return(html)
