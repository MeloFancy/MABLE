from collections import Counter
from sklearn.metrics import precision_score, recall_score, classification_report, accuracy_score

from processors.utils_ner import get_entities


class SeqEntityScore(object):
    def __init__(self, id2label, id2type, markup='bios'):
        self.id2label = id2label
        self.id2type = id2type
        self.markup = markup
        self.reset()

    def acc_and_f1(self, preds, labels, all_cates):
        class_info = {}
        class_preds = {}
        class_labels = {}
        tprecision = precision_score(y_true=labels, y_pred=preds, average='weighted')
        trecall = recall_score(y_true=labels, y_pred=preds, average='weighted')
        tf1 = 0. if trecall + tprecision == 0 else (2 * tprecision * trecall) / (tprecision + trecall)
        report = classification_report(labels, preds, labels=list(self.id2type.keys()), target_names=self.id2type.values(), digits=4, output_dict=True)
        taccuracy = accuracy_score(y_true=labels, y_pred=preds)
        for pred, label, cate in zip(preds, labels, all_cates):
            if cate in class_preds:
                class_preds[cate].append(pred)
                class_labels[cate].append(label)
            else:
                class_preds[cate] = []
                class_labels[cate] = []
                class_preds[cate].append(pred)
                class_labels[cate].append(label)
        for type_ in class_preds:
            preds = class_preds[type_]
            labels = class_labels[type_]
            precision = precision_score(y_true=labels, y_pred=preds, average='weighted')
            recall = recall_score(y_true=labels, y_pred=preds, average='weighted')
            f1 = 0. if recall + precision == 0 else (2 * precision * recall) / (precision + recall)
            accuracy = accuracy_score(y_true=labels, y_pred=preds)
            class_info[type_] = {'acc': round(accuracy, 4), 'pre': round(precision, 4), 'recall': round(recall, 4), 'f1': round(f1, 4)}
        return {
            "type_acc": taccuracy,
            "type_pre": tprecision,
            "type_recall": trecall,
            "type_f1": tf1,
        }, class_info, report

    def reset(self):
        self.origins = []
        self.founds = []
        self.rights = []

    def compute(self, origin, found, right):
        recall = 0 if origin == 0 else (right / origin)
        precision = 0 if found == 0 else (right / found)
        f1 = 0. if recall + precision == 0 else (2 * precision * recall) / (precision + recall)
        return recall, precision, f1

    def result(self):
        class_info = {}
        origin_counter = Counter([x[0] for x in self.origins])
        found_counter = Counter([x[0] for x in self.founds])
        right_counter = Counter([x[0] for x in self.rights])
        for type_, count in origin_counter.items():
            origin = count
            found = found_counter.get(type_, 0)
            right = right_counter.get(type_, 0)
            recall, precision, f1 = self.compute(origin, found, right)
            class_info[type_] = {'pre': round(precision, 4), 'recall': round(recall, 4), 'f1': round(f1, 4)}
        origin = len(self.origins)
        found = len(self.founds)
        right = len(self.rights)
        recall, precision, f1 = self.compute(origin, found, right)
        return {'ner_pre': precision, 'ner_recall': recall, 'ner_f1': f1}, class_info

    def update(self, label_paths, pred_paths, cate):
        '''
        labels_paths: [[],[],[],....]
        pred_paths: [[],[],[],.....]

        :param label_paths:
        :param pred_paths:
        :return:
        Example:
            >>> labels_paths = [['O', 'O', 'O', 'B-MISC', 'I-MISC', 'I-MISC', 'O'], ['B-PER', 'I-PER', 'O']]
            >>> pred_paths = [['O', 'O', 'B-MISC', 'I-MISC', 'I-MISC', 'I-MISC', 'O'], ['B-PER', 'I-PER', 'O']]
        '''
        for label_path, pre_path in zip(label_paths, pred_paths):
            label_entities = get_entities(label_path, self.id2label,self.markup)
            pre_entities = get_entities(pre_path, self.id2label,self.markup)

            label_entities = [[cate, beg, end] for _, beg, end in label_entities]
            pre_entities = [[cate, beg, end] for _, beg, end in pre_entities]
            self.origins.extend(label_entities)
            self.founds.extend(pre_entities)
            self.rights.extend([pre_entity for pre_entity in pre_entities if pre_entity in label_entities])


class SpanEntityScore(object):
    def __init__(self, id2label):
        self.id2label = id2label
        self.reset()

    def reset(self):
        self.origins = []
        self.founds = []
        self.rights = []

    def compute(self, origin, found, right):
        recall = 0 if origin == 0 else (right / origin)
        precision = 0 if found == 0 else (right / found)
        f1 = 0. if recall + precision == 0 else (2 * precision * recall) / (precision + recall)
        return recall, precision, f1

    def result(self):
        class_info = {}
        origin_counter = Counter([self.id2label[x[0]] for x in self.origins])
        found_counter = Counter([self.id2label[x[0]] for x in self.founds])
        right_counter = Counter([self.id2label[x[0]] for x in self.rights])
        for type_, count in origin_counter.items():
            origin = count
            found = found_counter.get(type_, 0)
            right = right_counter.get(type_, 0)
            recall, precision, f1 = self.compute(origin, found, right)
            class_info[type_] = {"acc": round(precision, 4), 'recall': round(recall, 4), 'f1': round(f1, 4)}
        origin = len(self.origins)
        found = len(self.founds)
        right = len(self.rights)
        recall, precision, f1 = self.compute(origin, found, right)
        return {'acc': precision, 'recall': recall, 'f1': f1}, class_info

    def update(self, true_subject, pred_subject):
        self.origins.extend(true_subject)
        self.founds.extend(pred_subject)
        self.rights.extend([pre_entity for pre_entity in pred_subject if pre_entity in true_subject])



