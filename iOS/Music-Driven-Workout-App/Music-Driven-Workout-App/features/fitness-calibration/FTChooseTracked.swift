////
////  FTChooseTracked.swift
////  Music-Driven-Workout-App
////
////  Created by Lucy Newman on 2/28/18.
////  Copyright © 2018 UChicago SoftCon. All rights reserved.
////
//
//import UIKit
//
//class FTChooseTracked: UIViewController {
//
//    var userid: String!
//    var reply: [[String:Any]] = [[String:Any]]()
//    var exList: [String] = [String]()
//
//    var viewModel = ViewModel()
//
//    @IBOutlet weak var trackedTable: UITableView?
//    
//    override func viewDidLoad() {
//        trackedTable?.allowsMultipleSelection = true
//        trackedTable?.dataSource = self.viewModel
//        trackedTable?.delegate = self
//        let request = APIRequest()
//        let qstr = "userid=" + userid + "&key=SoftCon2018"
//        request.submitPostLocal(route: "/api/fitness/tracked/", qstring: qstr) { (data, response, error) -> Void in
//            if let error = error {
//                fatalError(error.localizedDescription)
//            }
//            self.reply = request.parseJsonRespone(data: data!)!
//
//            //            names = reply.map { $0["name"] }
//            for rep in self.reply {
//                self.exList.append(rep["name"]! as! String)
//            }
//
//            DispatchQueue.main.async {
//
//            }
//            }.resume()
//
//    }
//
//    @IBAction func next(_ sender: Any) {
//    }
//
//    /*
//    // Only override draw() if you perform custom drawing.
//    // An empty implementation adversely affects performance during animation.
//    override func draw(_ rect: CGRect) {
//        // Drawing code
//    }
//    */
//
//}
//
//extension FTChooseTracked: UITableViewDelegate {
//    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
//        viewModel.items[indexPath.row].isSelected = true
//    }
//
//    func tableView(_ tableView: UITableView, didDeselectRowAt indexPath: IndexPath) {
//        viewModel.items[indexPath.row].isSelected = false
//    }
//}
//
