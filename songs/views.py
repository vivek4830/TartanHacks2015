
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader as templateLoader, RequestContext
from django.shortcuts import render

from songs.models import Song, YTVid
from songs.forms import SongForm, PlaylistForm

playlistID = 0

def http_client_error(x):
    print x
    return None

def mainIndex(request):
    form = PlaylistForm()

    return render(request, 'songs/index.html', {'form':form})

def index(request):
    """Play a YT video"""
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            # Process form data
            playlistID = form.cleaned_data['playlistID']
            print "playlist ID is: ", playlistID
            song_list = Song.objects.filter(playlistID__exact=playlistID,
                                            playlistPosition__exact=1)
            if (len(song_list) != 1):
                print "Bad playlist ID or playlist index"
                exit(1)
            Y = YTVid(song_list[0].songUrl)
            contextVars = {
                "video_title" : Y.title,
                "video_id"    : Y.id,
            }
            return HttpResponseRedirect("/songs/%s&tracknum=1" % playlistID)
    else:
        print "else"
        form = PlaylistForm()

    return render(request, "songs/index.html", contextVars)
    
def cmpPos(S1, S2):
    return cmp(S1.playlistPosition, S2.playlistPosition)
    
def playlist(request, playlist_id, playlist_index):
    """Process a playlist, starting with playlist_index"""
    try:
        i = int(playlist_index)
    except:
        http_client_error("Bad playlist index")
        
    prayrist = Song.objects.filter(playlistID__exact=playlist_id)
    if not(len(prayrist)):
        return http_client_error("Playlist empty")
    if not((0 < i) and (i <= len(prayrist))):
        return http_client_error("Bad playlist index")
    
    songList = sorted(prayrist, cmpPos)
    currentSong = prayrist[i-1] # zero-index
    Y = YTVid(currentSong.songUrl)
    contextVars = {
        "video_title"      : Y.title,
        "video_id"         : Y.id,
        "playlist_id"      : playlist_id,
        "current_position" : playlist_index,
        "next_track_num"   : (i % len(songList))+1,
        "song_list"        : songList
    }
    return render(request, "songs/autoplay.html", contextVars)

def addSong(request):
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            # Process form data from form.cleaned_data
            newTrackNum = len(Song.objects.filter(playlistID__exact=form.cleaned_data['playlistID']))
            currentSong = Song()
            currentSong.songName = form.cleaned_data['songName']
            currentSong.songUrl = form.cleaned_data['songUrl']
            currentSong.playlistID = form.cleaned_data['playlistID']
            currentSong.playlistPosition = newTrackNum
            currentSong.save()
            pl_id = currentSong.playlistID
            return HttpResponseRedirect("/songs/%d&tracknum=%d" %
                                        (pl_id, newTrackNum))
    else:
        form = SongForm()

    return render(request, 'songs/addSong.html', {'form': form})
