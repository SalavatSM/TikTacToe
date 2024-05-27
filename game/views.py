from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'game/index.html')


def play(request):
    if 'board' not in request.session:
        request.session['board'] = ['' for _ in range(9)]
        request.session['turn'] = 'X'
        request.session['winner'] = None
    return render(request, 'game/play.html')


@csrf_exempt
def move(request):
    if request.method == 'POST':
        position = int(request.POST['position'])
        board = request.session['board']
        turn = request.session['turn']

        if board[position] == '' and request.session['winner'] is None:
            board[position] = turn
            request.session['turn'] = 'O' if turn == 'X' else 'X'
            request.session['board'] = board

            winner = check_winner(board)
            if winner:
                request.session['winner'] = winner
                return JsonResponse({'status': 'win', 'winner': winner})

            if '' not in board:
                request.session['winner'] = 'Draw'
                return JsonResponse({'status': 'draw'})

            return JsonResponse({'status': 'move', 'board': board, 'turn': request.session['turn']})
        else:
            return JsonResponse({'status': 'invalid'})


@csrf_exempt
def reset(request):
    if request.method == 'POST':
        request.session.flush()
        return JsonResponse({'status': 'reset'})


def check_winner(board):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] and board[condition[0]] != '':
            return board[condition[0]]

    return None



