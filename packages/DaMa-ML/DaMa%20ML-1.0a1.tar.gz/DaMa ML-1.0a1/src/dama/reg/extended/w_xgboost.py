from dama.reg.wrappers import XGB, SKLP
import xgboost as xgb


class Xgboost(XGB):

    def prepare_model(self, obj_fn=None, num_steps: int = 0, model_params=None, batch_size: int = None):
        data_train = self.ds[self.data_groups["data_train_group"]].to_ndarray()
        target_train = self.ds[self.data_groups["target_train_group"]].to_ndarray()
        data_val = self.ds[self.data_groups["data_validation_group"]].to_ndarray()
        target_val = self.ds[self.data_groups["target_validation_group"]].to_ndarray()
        d_train = xgb.DMatrix(data_train, target_train)
        d_valid = xgb.DMatrix(data_val, target_val)
        watchlist = [(d_train, 'train'), (d_valid, 'valid')]
        nrounds = num_steps
        xgb_model = xgb.train(model_params, d_train, nrounds, watchlist, early_stopping_rounds=int(nrounds/2),
                              feval=obj_fn, maximize=True, verbose_eval=100)
        return self.ml_model(xgb, bst=xgb_model)

    def feature_importance(self):
        pass


class XgboostSKL(SKLP):
    def prepare_model(self, obj_fn=None, num_steps: int = 0, model_params=None, batch_size: int = None):
        if model_params is None:
            model_params = dict(seed=3, n_estimators=25)
        model = xgb.XGBClassifier(**model_params)
        reg_model = model.fit(self.ds[self.data_groups["data_train_group"]].to_ndarray(),
                              self.ds[self.data_groups["target_train_group"]].to_ndarray())
        return self.ml_model(reg_model)
