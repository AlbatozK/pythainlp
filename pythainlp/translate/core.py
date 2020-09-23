# -*- coding: utf-8 -*-
import os
import tarfile
from collections import defaultdict
from functools import partial

from pythainlp.corpus import download, get_corpus_path
from pythainlp.tokenize import word_tokenize as th_word_tokenize
from pythainlp.tools import get_full_data_path, get_pythainlp_data_path

from fairseq.models.transformer import TransformerModel
from sacremoses import MosesDetokenizer, MosesTokenizer

en_word_detokenize = MosesDetokenizer("en")
en_word_tokenize = MosesTokenizer("en")
th_word_tokenize = partial(th_word_tokenize, keep_whitespace=False)

model = None
model_name = None


def _download_install(name):
    if get_corpus_path(name) is None:
        download(name, force=True, version="1.0")
        tar = tarfile.open(get_corpus_path(name), "r:gz")
        tar.extractall()
        tar.close()
    if not os.path.exists(get_full_data_path(name)):
        os.mkdir(get_full_data_path(name))
        with tarfile.open(get_corpus_path(name)) as tar:
            tar.extractall(path=get_full_data_path(name))


def download_model_all() -> None:
    """
    Download Model
    """
    _download_install("scb_th_en")
    _download_install("scb_en_th")


def _get_translate_path(
    model: str, *path1: str
) -> str:
    path = os.path.join(get_full_data_path(model), *path1)
    return path


def _scb_en_th_model():
    global model, model_name
    _download_install(
        "scb_en_th"
    )  # SCB_1M-MT_OPUS+TBASE_en-th_moses-newmm_space_130000-130000_v1.0.tar.gz
    if model_name != "scb_en_th":
        del model
        model = TransformerModel.from_pretrained(
            model_name_or_path=_get_translate_path(
                "scb_en_th",
                "SCB_1M-MT_OPUS+TBASE_en-th_moses-newmm_space_130000-130000_v1.0",
                "models",
            ),
            checkpoint_file="checkpoint.pt",
            data_name_or_path=_get_translate_path(
                "scb_en_th",
                "SCB_1M-MT_OPUS+TBASE_en-th_moses-newmm_space_130000-130000_v1.0",
                "vocab",
            ),
        )
        model_name = "scb_en_th"


def _scb_en_th_translate(text: str) -> str:
    global model, model_name
    _scb_en_th_model()
    tokenized_sentence = " ".join(en_word_tokenize.tokenize(text))
    hypothesis = model.translate(tokenized_sentence)
    hypothesis = hypothesis.replace("▁", " ")
    return hypothesis


def _scb_th_en_model():
    global model, model_name
    _download_install(
        "scb_th_en"
    )  # SCB_1M-MT_OPUS+TBASE_th-en_spm-moses_16000-130000_v1.0.tar.gz
    if model_name != "scb_th_en":
        del model
        model = TransformerModel.from_pretrained(
            model_name_or_path=_get_translate_path(
                "scb_th_en",
                "SCB_1M-MT_OPUS+TBASE_th-en_spm-moses_16000-130000_v1.0",
                "models",
            ),
            checkpoint_file="checkpoint.pt",
            data_name_or_path=_get_translate_path(
                "scb_th_en",
                "SCB_1M-MT_OPUS+TBASE_th-en_spm-moses_16000-130000_v1.0",
                "vocab",
            ),
            bpe="sentencepiece",
            sentencepiece_vocab=_get_translate_path(
                "scb_th_en",
                "SCB_1M-MT_OPUS+TBASE_th-en_spm-moses_16000-130000_v1.0",
                "bpe",
                "spm.th.model",
            ),
        )
        model_name = "scb_th_en"


def _scb_th_en_translate(text: str) -> str:
    global model, model_name
    _scb_th_en_model()
    hypothesis = model.translate(text,beam=4)
    return hypothesis


def translate(text: str, source: str, target: str) -> str:
    """
    Translate Language

    :param str text: input text in source language
    :param str source: source language ("en" or "th")
    :param str target: target language ("en" or "th")

    :return: translated text in target language
    :rtype: str
    """
    hypothesis = None

    if source == "th" and target == "en":
        hypothesis = _scb_th_en_translate(text)
    elif source == "en" and target == "th":
        hypothesis = _scb_en_th_translate(text)
    else:
        return ValueError("the combination of the arguments isn't allowed.")

    return hypothesis