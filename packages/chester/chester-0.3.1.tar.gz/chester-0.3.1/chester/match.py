import chess
import chess.engine
import chess.pgn
import datetime


def play_match(
    engine1,
    engine2,
    time_control,
    fen=chess.STARTING_FEN,
    engine1_options=dict(),
    engine2_options=dict(),
):
    """Play a match between the given engines with a given time control.

    Arguments
    ---------
    engine1, engine2: str
        Executable of the UCI engines to play. Engine1 will play white.
    time_control: chester.timecontrol.TimeControl
        A TimeControl instance describing the time control to use.
    fen: str, optional
        Starting position in FEN notation. Default is the standard opening position.
    engine1_options, engine2_options: dict, optional
        A dictionary with options to set for each engine. The key should be the
        name of the option as provided by the engine. To see available options you may
        do:
        ``` python
        engine = chess.engine.SimpleEngine.popen_uci("name-of-executable")
        print(engine.options)
        ```
        See https://python-chess.readthedocs.io/en/latest/engine.html#chess.engine.EngineProtocol.options

        Only the options that match the engines option names will be configured.

    Returns
    -------
        A `chess.pgn.Game` instance describing the game.
    """
    engine1 = chess.engine.SimpleEngine.popen_uci(engine1)
    engine2 = chess.engine.SimpleEngine.popen_uci(engine2)

    # Apply
    for engine, options in zip([engine1, engine2], [engine1_options, engine2_options]):
        available = engine1.options
        options = {
            k: v
            for k, v in options.items()
            if k in available and not available[k].is_managed()
        }
        engine.configure(options)

    result = None
    board = chess.Board(fen)
    time_control._start_new_game(side_to_move=board.turn)
    current_player = engine1 if board.turn == chess.WHITE else engine2
    while not board.is_game_over():
        output = current_player.play(
            board,
            chess.engine.Limit(
                white_clock=time_control.wtime,
                black_clock=time_control.btime,
                white_inc=time_control.increment,
                black_inc=time_control.increment,
            ),
        )

        player_flagged = time_control._signal_move_made()

        if player_flagged:
            if board.has_insufficient_material(not board.turn):
                result = "1/2-1/2"
            else:
                result = "0-1" if board.turn == chess.WHITE else "1-0"
            break

        board.push(output.move)
        current_player = engine1 if board.turn == chess.WHITE else engine2

    pgn = chess.pgn.Game.from_board(board)
    pgn.headers["White"] = engine1.id.get("name")
    pgn.headers["Black"] = engine2.id.get("name")
    pgn.headers["Date"] = datetime.datetime.today().strftime("%Y-%m-%d")
    if fen != chess.STARTING_FEN:
        pgn.headers["FEN"] = fen

    if result is not None:
        pgn.headers["Result"] = result

    engine1.quit()
    engine2.quit()

    return pgn
