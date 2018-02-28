//
//  FTChooseTracked.swift
//  Music-Driven-Workout-App
//
//  Created by Lucy Newman on 2/28/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

private let reuseIdentifier = "Cell"

class FTChooseTracked: UIViewController {

    var viewModel = ViewModel()
    let items = ["Hello there", "my people"]
    
    var userid: String = "1"
    var category: String = ""
    var numEx: Int = 1
    var reply: [[String:Any]] = [[String:Any]]()
    var exList: [String] = [String]()
    var exChoices: [Int] = [Int]()
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.destination is FTSummaryViewController
        {
            let vc = segue.destination as? FTSummaryViewController
            //data to send
            vc?.category = category
            vc?.userid = userid
            vc?.numEx = numEx
            vc?.exChoices = exChoices
        }
    }
    
    @IBOutlet weak var instructions: UILabel!
    @IBOutlet weak var tableView: UITableView?
    @IBOutlet weak var nextButton: UIButton?
    
    override func viewDidLoad() {
        super.viewDidLoad()

        instructions.text = "Choose up to \(numEx) tracked exercise"
        if numEx != 1 {
            instructions.text? += "s"
        }

        let qstr = "userid=\(userid)&categories=\(category)&key=SoftCon2018"
        let request = APIRequest()
        
        request.submitPostLocal(route: "/api/fitness/tracked/", qstring: qstr) { (data, response, error) -> Void in
            if let error = error {
                fatalError(error.localizedDescription)
            }
            self.reply = request.parseJsonRespone(data: data!)!

            let vmitems = self.reply.map { ViewModelItem(item: Model(title: $0["name"] as! String, data: $0)) }
            self.viewModel.setItems(items: vmitems)
            
            
            DispatchQueue.main.async {
                self.tableView?.register(CustomCell.nib, forCellReuseIdentifier: CustomCell.identifier)
                self.tableView?.dataSource = self.viewModel
                self.tableView?.delegate = self.viewModel
                self.tableView?.estimatedRowHeight = 100
                self.tableView?.rowHeight = UITableViewAutomaticDimension
                self.tableView?.allowsMultipleSelection = true
                self.tableView?.separatorStyle = .none
            }
            
            }.resume()
        

        
        
        viewModel.didToggleSelection = { [weak self] hasSelection in
            self?.nextButton?.isEnabled = hasSelection
        }
        
    }
    
    @IBAction func next(_ sender: Any) {
        exChoices = viewModel.selectedItems.map{ $0.data["id"] as! Int}
        tableView?.reloadData()
    }
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

}
